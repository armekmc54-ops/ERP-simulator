"""Load an isolated AP demonstration and verify actual Cypher decisions."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from neo4j import GraphDatabase
from rules import classify_invoice

HERE = Path(__file__).parent
BASE = dict(active=True, ordered=10, received=10, invoiced=10,
            order_price=5000, invoice_price=5000, has_receipt=True)
CASES = [
    dict(id='AP-01'), dict(id='AP-02', received=4, invoiced=4),
    dict(id='AP-03', invoiced=11), dict(id='AP-04', invoice_price=5500),
    dict(id='AP-05', has_receipt=False), dict(id='AP-06', active=False),
    dict(id='AP-07', invoiced=0),
]


def main():
    rows = [BASE | case for case in CASES]
    with GraphDatabase.driver(os.environ['NEO4J_URI'], auth=(
            os.environ['NEO4J_USERNAME'], os.environ['NEO4J_PASSWORD'])) as driver:
        driver.verify_connectivity()
        def query(cypher, **params):
            result = driver.execute_query(cypher, database_='neo4j', **params)
            return [r.data() for r in result.records]
        query((HERE / 'schema.cypher').read_text(encoding='utf-8'))
        load = (HERE / 'load.cypher').read_text(encoding='utf-8')
        query(load, rows=rows)
        counts = query('MATCH (n:APDemo) RETURN count(n) AS nodes')
        links = query('MATCH (:APDemo)-[r]->(:APDemo) RETURN count(r) AS relationships')
        query(load, rows=rows)
        assert counts == query('MATCH (n:APDemo) RETURN count(n) AS nodes'), 'Duplicate nodes'
        assert links == query('MATCH (:APDemo)-[r]->(:APDemo) RETURN count(r) AS relationships'), 'Duplicate relationships'
        decisions = query((HERE / 'validate.cypher').read_text(encoding='utf-8'))
        expected = {row['id']: classify_invoice(row) for row in rows}
        assert {r['invoice']: r['decision'] for r in decisions} == expected, decisions
        assert sum(r['payment_allowed'] for r in decisions) == 2
        events = []
        for decision in decisions:
            event_id = 'APMatch-' + decision['invoice']
            query('''MATCH (i:APDemo:Invoice {id: $invoice})
                MERGE (e:APDemo:AgentReport {id: $event_id})
                SET e.agent = 'APValidationAgent', e.activity = 'THREE_WAY_MATCH',
                    e.decision = $decision, e.payment_allowed = $allowed,
                    e.reported_at = datetime()
                MERGE (e)-[:REPORTS_ON]->(i)''',
                invoice=decision['invoice'], event_id=event_id,
                decision=decision['decision'], allowed=decision['payment_allowed'])
            events.append(dict(event_id=event_id, agent='APValidationAgent', **decision))
        assert query('MATCH (e:APDemo:AgentReport) RETURN count(e) AS count')[0]['count'] == len(rows)
        evidence = dict(status='passed', executed_at_utc=datetime.now(timezone.utc).isoformat(),
                        source_commit=os.getenv('GITHUB_SHA'), cases=decisions,
                        idempotent=True, agent_reports=events)
        output = HERE / 'evidence'
        output.mkdir(exist_ok=True)
        rendered = json.dumps(evidence, ensure_ascii=False, indent=2)
        (output / 'results.json').write_text(rendered + '\n', encoding='utf-8')
        print(rendered)
        summary = os.getenv('GITHUB_STEP_SUMMARY')
        if summary:
            with open(summary, 'a', encoding='utf-8') as file:
                file.write('## AP: conciliación de tres vías\n\n| Factura | Decisión | Permite pago |\n|---|---|---|\n')
                for row in decisions:
                    file.write(f"| {row['invoice']} | {row['decision']} | {row['payment_allowed']} |\n")


if __name__ == '__main__':
    main()

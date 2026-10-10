// Slide content for COURSE_GUIDE.html. One object per episode; one object per slide.
// Slide kinds: idea (default), code, do, quiz.

const ROOT = "/Users/fakhruddinkhambaty/Desktop/FK/DataEngineeringAndAnalyticsByFK";
const ENV = `cd ${ROOT}\nsource .venv/bin/activate\nset -a; source .env; set +a`;
const DBT = ENV + "\ncd 04_dbt_meridian_dw";

function esc(s){ return String(s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }
function flow(items){
  return `<div class="flow">` + items.map(([tag, title, sub, color]) =>
    `<div class="box"${color ? ` style="border-top:6px solid ${color}"` : ""}><em>${tag}</em><b>${title}</b><span>${sub}</span></div>`
  ).join("") + `</div>`;
}
function pair(badTitle, bad, goodTitle, good){
  return `<div class="pair"><div class="bad"><b>${badTitle}</b>${bad}</div><div class="good"><b>${goodTitle}</b>${good}</div></div>`;
}
function tbl(head, rows){
  return `<table><tr>${head.map(h => `<th>${h}</th>`).join("")}</tr>` +
    rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join("")}</tr>`).join("") + `</table>`;
}
function pre(code){ return `<pre class="snip">${esc(code)}</pre>`; }
function note(text){ return `<p class="note">${text}</p>`; }

const EP = [
// ================================================================ E0
{id:"e0", code:"E0", mins:"45 min", color:"#44403c", title:"The problem, then the picture",
 slides:[
  {h:"A bank that cannot answer a simple question",
   say:"How much did Mumbai customers spend on Amazon during the sale, in dollars? And who is allowed to see that number?",
   plain:["The bank's database is built to take payments fast. It is not built to answer questions across five million payments.",
          "Answering needs the data copied somewhere else, cleaned, joined, converted to dollars, and locked so each person sees only their rows.",
          "That 'somewhere else' and the steps to get there are the whole course."],
   art: flow([["Ask","Mumbai","Amazon, sale week, in USD","#336791"],["Then","Who may see it","CEO, branch manager, staff, customer","#6d28d9"]]) +
        note("Open on this question. Every later episode answers one part of it.")},
  {h:"What 'done' means, before any tool",
   say:"These five promises are the requirements. Every design choice later points back to one of them.",
   art: tbl(["Promise","How we keep it"],[
     ["Fresh: at most 15 minutes behind the bank","Airflow loads every 5 minutes; the health check fails above 15"],
     ["Correct: warehouse totals equal the bank's","reconcile_with_pandas.py and a dbt reconciliation test"],
     ["History: a customer's past is kept","Snapshots and SCD2 dimensions"],
     ["Private: each person sees only their rows","Row access policies and masking in Snowflake"],
     ["Cheap: a free trial can run it","Extra-small warehouses that pause after 60 seconds"]])},
  {wide:true, h:"The six rooms",
   say:"A payment is born in the till, carried by a courier, dropped in an inbox, cooked in a kitchen, put on a shelf, and asked about at the front desk.",
   art: tbl(["Room","Tool","What it does here"],[
     ["Till","Postgres in Docker","The bank's live database. Takes payments."],
     ["Courier","Python script","Copies only the rows that changed"],
     ["Inbox","Snowflake MERIDIAN_RAW","Keeps every copy it was handed. Bronze."],
     ["Kitchen","dbt","Cleans and joins with SQL inside Snowflake. Silver."],
     ["Shelf","Snowflake MARTS","Facts and dimensions people query. Gold."],
     ["Front desk","Streamlit + Cortex Analyst","Turns an English question into SQL"],
     ["Alarm clock","Airflow","Runs the courier and the kitchen on a timer"]])},
  {wide:true, h:"Technology, language, working surface, output",
   say:"A tool is not a language, and an IDE is not a file format. This is the map we will use for the whole series.",
   art: tbl(["Technology","What we type","Where we work","What it produces"],[
     ["PostgreSQL","SQL and PL/pgSQL","DBeaver; Docker runs the server","operational bank rows"],
     ["Python","Python","Cursor and Terminal","Parquet files and control records"],
     ["Snowflake","SQL","Snowsight","raw tables, policies and queries"],
     ["dbt","SQL, Jinja and YAML","Cursor; dbt CLI in Terminal","tested facts, dimensions and docs"],
     ["Airflow","Python","Cursor; Airflow UI","scheduled runs, retries and alerts"],
     ["Streamlit","Python","Cursor or Streamlit in Snowflake","the governed app"],
     ["Terraform","HCL","Cursor; Terraform CLI","roles, warehouses and cost guardrails"],
     ["GitHub Actions","YAML","GitHub","automatic checks on every change"]]) +
     note("Parquet is a file format. Docker is a runtime. Cursor is a VS Code-compatible editor. None is a programming language.")},
  {wide:true, h:"Where each piece physically runs",
   say:"Three places: my laptop, Docker containers on my laptop, and Snowflake in the cloud. Most confusion comes from forgetting which one you are in.",
   art: `<div class="where3">
     <div><b>Your Mac</b><span>Python loader, dbt commands, Streamlit app, DBeaver, the private key in ~/.ssh</span></div>
     <div><b>Docker on your Mac</b><span>meridian_postgres (port 5432). Airflow containers: scheduler, workers, its own metadata Postgres</span></div>
     <div><b>Snowflake cloud</b><span>MERIDIAN_RAW, MERIDIAN_ANALYTICS, warehouses, policies, Cortex</span></div></div>` +
     note("Inside an Airflow container, 'localhost' means the container itself. That is why its copy of .env says host.docker.internal.")},
  {h:"Grain: say what one row is",
   say:"Before building a table, say out loud what one row means. If you cannot, the table will double-count.",
   art: tbl(["Table","One row is"],[
     ["fct_transactions","one payment, newest status"],
     ["dim_customer","one version of one customer"],
     ["fct_monthly_account_balance","one account at the end of one month"],
     ["fct_loan_applications","one loan application, from submitted to decided"],
     ["fct_next_best_offer","one customer and the one offer to make"]])},
  {h:"Name the option you rejected",
   say:"We copy changes using a timestamp bookmark, not by reading the database log with Debezium. It is simpler to teach. Two triggers make it safe. Debezium is the production upgrade.",
   plain:["The decision is written in 00_architecture/adr/0001-watermark-cdc-before-log-based.md.",
          "Interviewers ask 'why not X'. A written decision record is the answer."]},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why can't analysts just query Postgres directly?","It is built for fast single payments. Big scans slow the bank down, it has no history of customer changes, and it has no per-person row rules."],
   ["Which three places run code in this project?","The Mac, Docker containers on the Mac, and Snowflake."],
   ["What is the grain of fct_transactions?","One row per transaction_id, with its latest status."]]}
 ]},

// ================================================================ MEDALLION
{id:"med", code:"M", mins:"20 min", color:"#a16207", title:"Medallion: bronze, silver, gold here",
 slides:[
  {h:"Medallion is a promise about how clean data is",
   say:"Bronze is exactly what arrived. Silver is cleaned: one row per thing, proper types. Gold is shaped for a question a person asks.",
   plain:["Groceries: bronze is the delivery box, unopened. Silver is washed, chopped, labelled tubs. Gold is the plated dish.",
          "You never cook from the box, and you never throw the box away until you are sure the dish is right."],
   art: `<div class="medal"><div class="b">BRONZE<small>as delivered</small></div><div class="s">SILVER<small>cleaned</small></div><div class="g">GOLD<small>ready to serve</small></div><i class="dot"></i></div>`},
  {wide:true, h:"Exactly where each layer lives in this project",
   say:"Our folders say raw, staging, marts. That is Kimball naming. Underneath, it is bronze, silver, gold.",
   art: tbl(["Layer","Snowflake location","Built by","Example"],[
     ["<b class='bz'>Bronze</b>","MERIDIAN_RAW.POSTGRES_CORE, POSTGRES_REF, POSTGRES_CDC","Python: PUT and COPY","RAW…POSTGRES_CORE.TRANSACTIONS"],
     ["<b class='sv'>Silver</b>","MERIDIAN_ANALYTICS.STAGING, INTERMEDIATE, SNAPSHOTS","dbt","stg_postgres__transactions, int_transactions_with_fx, snap_customers"],
     ["<b class='gd'>Gold</b>","MERIDIAN_ANALYTICS.MARTS","dbt","fct_transactions, dim_customer, fct_next_best_offer"],
     ["On top of gold","MARTS.SV_MERIDIAN_BANK","you, in SQL","the semantic view the English app reads"]]) +
     note("In dev, dbt writes silver and gold into DBT_FK_STAGING, DBT_FK_MARTS and so on, so practice never overwrites production.")},
  {wide:true, h:"Follow one payment through the three layers",
   say:"Payment 101 was created pending, then settled. Bronze has every copy. Silver keeps the newest. Gold adds the who, where and when.",
   art: `<div class="layer bz-bg"><b>Bronze · 3 rows</b>${pre(`record (VARIANT)                                   _extracted_at
{"transaction_id":101,"status":"PENDING",...}      09:00
{"transaction_id":101,"status":"POSTED", ...}      09:05
{"transaction_id":101,"status":"POSTED", ...}      10:00  (re-sent after a retry)`)}</div>
   <div class="layer sv-bg"><b>Silver · 1 row, typed</b>${pre(`transaction_id 101 | status POSTED | amount 2400.00 INR | amount_reporting 28.80 USD`)}</div>
   <div class="layer gd-bg"><b>Gold · 1 row, joined</b>${pre(`transaction_id 101 | date_key 20260915 | customer_key a91f… | branch_key 7c2e… | amount_reporting 28.80`)}</div>` +
   note("The amounts and keys are illustrative. Run the next slide's query to see a real payment.")},
  {wide:true, h:"The rules of each layer",
   say:"Each layer has a job and a thing it is not allowed to do.",
   art: tbl(["Layer","Allowed","Not allowed"],[
     ["Bronze","Append rows. Add _extracted_at, _batch_id, _source_file.","Update, delete, fix, or reshape anything"],
     ["Silver · staging","Rename, cast types, keep the newest version, drop deleted rows","Joins between business tables"],
     ["Silver · intermediate","Reusable logic: FX conversion, primary account holder","Being read by people or the app"],
     ["Gold · marts","Facts, dimensions, tests, contracts, row policies","Being skipped: people and the app read only gold"]])},
  {h:"Why bronze never changes",
   say:"If I find a bug in silver, I fix the SQL and rebuild from bronze. I never go back to the bank's database. That is what bronze buys.",
   plain:["Raw has MORE rows than Postgres. That is not a bug. It is every version, including rows later deleted in the bank.",
          "The decision is ADR 0002, append-only VARIANT raw.",
          "VARIANT means a JSON-like column. A new column in Postgres does not break the load; it just appears inside record."],
   art: pair("If bronze was edited","a bad fix is permanent; you must reload from the bank","Because bronze is append-only","fix the dbt model, run dbt build --full-refresh on it, done")},
  {h:"Medallion and Kimball are not rivals",
   say:"Medallion says how clean each floor of the building is. Kimball says how the top floor is laid out: facts in the middle, dimensions around them.",
   art: `<div class="building"><div class="fl g">Gold floor · Kimball star: fct_transactions in the middle, dim_customer, dim_account, dim_branch, dim_date around it</div><div class="fl s">Silver floor · staging views and intermediate logic</div><div class="fl b">Bronze floor · raw VARIANT tables</div></div>` +
   note("ADR 0003 chose Kimball for the presentation layer. That is why the gold schema is called MARTS.")},
  {k:"do", h:"See one real payment in all three layers", where:"Snowsight · role MERIDIAN_TRANSFORMER · warehouse WH_TRANSFORM_XS",
   cmd:`USE ROLE MERIDIAN_TRANSFORMER;
USE WAREHOUSE WH_TRANSFORM_XS;

SET txn_id = (
  SELECT record:transaction_id::number
  FROM MERIDIAN_RAW.POSTGRES_CORE.TRANSACTIONS
  GROUP BY 1 HAVING COUNT(*) > 1
  LIMIT 1);

-- Bronze: every copy that arrived
SELECT record:status::string AS status, _extracted_at, _batch_id
FROM MERIDIAN_RAW.POSTGRES_CORE.TRANSACTIONS
WHERE record:transaction_id::number = $txn_id
ORDER BY _extracted_at;

-- Silver: the newest copy, typed
SELECT transaction_id, status, amount, currency_code, updated_at
FROM MERIDIAN_ANALYTICS.STAGING.STG_POSTGRES__TRANSACTIONS
WHERE transaction_id = $txn_id;

-- Gold: joined to dimensions, converted to USD
SELECT transaction_id, date_key, customer_key, branch_key, amount_local, amount_reporting
FROM MERIDIAN_ANALYTICS.MARTS.FCT_TRANSACTIONS
WHERE transaction_id = $txn_id;`,
   happened:["SET stores one transaction id that has more than one copy in bronze.",
             "The first query shows two or more rows: the copies.",
             "The second shows exactly one row: silver kept the newest.",
             "The third shows one row with keys to customer, branch and date, and the USD amount."],
   see:"Bronze: two or more rows. Silver: one. Gold: one.",
   trap:"If txn_id is NULL, no payment has changed since the load. In DBeaver run SELECT * FROM core.sim_tick(500); then load once more with the Python command from E4."},
  {k:"quiz", h:"Check yourself", qs:[
   ["The FX conversion is wrong. Which layer do you fix? Do you reload from Postgres?","Silver: int_transactions_with_fx. No reload. Rebuild from bronze: dbt build -s int_transactions_with_fx+ --full-refresh."],
   ["Why does raw have more rows than Postgres?","Bronze keeps every version, including deleted rows. Silver keeps one per id."],
   ["Which layer does the Streamlit app read?","Gold, through the semantic view on MARTS."],
   ["Why are the folders called raw, staging, marts and not bronze, silver, gold?","Kimball naming for the same three layers. ADR 0003."]]}
 ]},

// ================================================================ E1
{id:"e1", code:"E1", mins:"50 min", color:"#336791", title:"The bank's live database",
 slides:[
  {h:"OLTP: built to take one payment fast",
   say:"Postgres here is the bank's till. It is tuned to insert and update single rows. Analytics never write back into it.",
   art: pair("OLTP · Postgres","many tiny writes, one customer at a time, current state only","OLAP · Snowflake","few huge reads across millions of rows, with history") +
        note("That difference is why we copy data out instead of querying the till.")},
  {h:"Three schemas, twenty tables",
   say:"ref is the lists the bank looks up, such as currency and country. core is the customers, accounts and payments. cdc is a notebook of deletes. Once a row is gone, Python has nothing left to copy, so a trigger writes the id into cdc.deleted_records first.",
   art: tbl(["Schema","Tables"],[
     ["ref","currencies, countries, fx_rates, channels, products, merchants, sale_events, offer_catalog"],
     ["core","branches, employees, customers, accounts, account_holders, transactions, loan_applications, customer_features, card_applications, credit_cards, card_authorizations"],
     ["cdc","deleted_records"]])},
  {wide:true, h:"How the tables connect",
   say:"A customer can hold many accounts, and an account can have joint holders, so account_holders sits between them. Every payment belongs to one account.",
   art: `<div class="er"><span>customers</span><i>⇄</i><span>account_holders</span><i>⇄</i><span>accounts</span><i>→</i><span>transactions</span></div>
         <div class="er"><span>branches</span><i>→</i><span>customers (home branch)</span></div>
         <div class="er"><span>credit_cards</span><i>→</i><span>card_authorizations</span><i>→</i><span>merchants</span></div>` +
        note("In DBeaver: right-click schema core, then View Diagram. Show this on camera.")},
  {h:"The courier needs two promises",
   say:"The courier asks: what changed since last time? It can only trust the answer if every update moves updated_at and every delete is written down.",
   art: flow([["Promise 1","updated_at always moves","BEFORE UPDATE trigger","#336791"],["Promise 2","deletes are logged","AFTER DELETE trigger into cdc.deleted_records","#b45309"]]) +
        note("Without promise 1, an app that forgets to set updated_at hides a change forever. Without promise 2, a deleted row stays in the warehouse forever.")},
  {k:"code", h:"The two trigger functions", file:"01_source_postgres/04_cdc_triggers.sql",
   lines:[
    [`CREATE OR REPLACE FUNCTION cdc.set_updated_at() RETURNS trigger`,"A function that runs on every UPDATE"],
    [`  NEW.updated_at := clock_timestamp();`,"Stamp the row with the real time now. clock_timestamp, not now(): now() is frozen for the whole transaction."],
    [`  RETURN NEW;`,"Write the stamped row"],
    [`CREATE OR REPLACE FUNCTION cdc.log_delete() RETURNS trigger`,"A function that runs on every DELETE"],
    [`  EXECUTE format('SELECT ($1).%I::text', TG_ARGV[0]) INTO v_pk USING OLD;`,"Read the deleted row's id. The id column name is passed in, so one function serves all 18 tables."],
    [`  INSERT INTO cdc.deleted_records (schema_name, table_name, pk_value, deleted_at)`,"Write which row went, and when"],
    [`  RETURN OLD;`,"Let the delete happen"]]},
  {h:"The simulator makes the bank alive",
   say:"A static database proves nothing. sim_tick inserts payments, settles pending ones, changes some customers, deletes a few rows, and runs card activity.",
   art: tbl(["Step in sim_tick","Why it matters for teaching"],[
     ["post_transactions","new rows: the courier must pick them up"],
     ["settle_pending","PENDING becomes POSTED: an update, so silver must keep the newest"],
     ["customer_changes","a segment changes: snapshots record a new version"],
     ["hard_deletes","rows vanish: the delete log and the post-hook must remove them"],
     ["card steps","authorizations, some with injected fraud patterns the rules must catch"]]) +
     note("SELECT * FROM core.sim_tick(500) runs once. simulate_activity.py loops every 5 seconds until Ctrl+C.")},
  {k:"do", h:"Start Postgres", where:"Terminal",
   cmd:`cd ${ROOT}
docker compose -f 01_source_postgres/docker-compose.postgres.yml up -d
docker ps --filter name=meridian_postgres`,
   happened:["cd goes to the project folder, where the compose file lives.","up -d starts the Postgres container in the background.","docker ps shows that it is running."],
   see:"Container meridian_postgres is Up, port 5432.",
   trap:"Docker Desktop must be running first. Look for the whale icon in the menu bar."},
  {k:"do", h:"Create the database, then point DBeaver at it", where:"DBeaver",
   cmd:`Open ${ROOT}/01_source_postgres/00_create_database.sql
Turn Auto-commit ON. Execute SQL Script.
Edit the connection: Database = meridian_core. Test. Reconnect.`,
   happened:["The script creates an empty database called meridian_core.","Changing the connection makes every later script run inside that database."],
   see:"The editor's database selector shows meridian_core.",
   trap:"If you skip the reconnect, the next scripts build the tables inside the default postgres database."},
  {k:"do", h:"Build and fill the bank, in this order", where:"DBeaver · meridian_core · Execute SQL Script on each file",
   cmd:`${ROOT}/01_source_postgres/01_ddl_core_schema.sql
${ROOT}/01_source_postgres/02_seed_reference_data.sql
${ROOT}/01_source_postgres/03_seed_bulk_data.sql
${ROOT}/01_source_postgres/07_ddl_cards.sql
${ROOT}/01_source_postgres/04_cdc_triggers.sql
${ROOT}/01_source_postgres/05_dml_simulator_functions.sql
${ROOT}/01_source_postgres/08_seed_cards.sql
${ROOT}/01_source_postgres/09_card_simulator.sql`,
   happened:["01 creates the empty tables.","02 adds branches, currencies, FX rates.","03 generates 200,000 customers and 5 million payments with pure SQL. Slow: record before the episode.",
             "07 adds card tables.","04 attaches the triggers to all tables, including the card tables, which is why it runs after 07.","05 and 09 install the simulators. 08 loads card history."],
   see:"Each script ends with no error.",
   trap:"Running 04 before 07 leaves the card tables without triggers."},
  {k:"do", h:"Prove the bank's size, then make it move", where:"DBeaver",
   cmd:`SELECT (SELECT count(*) FROM core.branches) branches,
       (SELECT count(*) FROM core.customers) customers,
       (SELECT count(*) FROM core.accounts) accounts,
       (SELECT count(*) FROM core.transactions) txns,
       (SELECT count(*) FROM core.loan_applications) loans;
SELECT * FROM core.sim_tick(500);`,
   happened:["The first query counts five tables in one row.","sim_tick runs every simulator step once and reports how many rows each touched."],
   see:"520 · 200000 · about 300000 · 5000000 · 60000. Then one row per simulator step.",
   trap:"Run the count before sim_tick. The simulator adds and deletes rows, so later counts differ."},
  {k:"code", h:"One SQL lesson to show live", file:"01_source_postgres/06_sql_lessons.sql",
   lines:[
    [`SELECT 1 WHERE 1 NOT IN (2, NULL);`,"Returns zero rows. Surprising on purpose."],
    [`-- 1 <> 2 is TRUE, 1 <> NULL is UNKNOWN`,"NOT IN is a chain of 'not equal' checks joined by AND"],
    [`-- TRUE AND UNKNOWN = UNKNOWN`,"UNKNOWN is not TRUE, so the row is dropped"],
    [`-- use NOT EXISTS instead`,"NOT EXISTS ignores NULLs and gives the answer people expect"]]},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why clock_timestamp() and not now()?","now() is fixed for the whole transaction. Two updates in one transaction would share a time and the courier could skip one."],
   ["How does the warehouse learn about a deleted row?","The delete trigger writes it to cdc.deleted_records. That table is copied like any other, and dbt deletes the matching rows."],
   ["Why must 04_cdc_triggers.sql run after 07_ddl_cards.sql?","04 attaches triggers to the card tables, which only exist after 07."]]}
 ]},

// ================================================================ E2
{id:"e2", code:"E2", mins:"45 min", color:"#6d28d9", title:"Draw the warehouse before you build it",
 slides:[
  {h:"Four questions, in order",
   say:"What business process? What is one row? What describes it? What do we measure? Answer these on paper before opening Snowflake.",
   art: flow([["1","Process","a payment happens","#6d28d9"],["2","Grain","one row per payment","#6d28d9"],["3","Dimensions","who, which account, where, when, which currency","#6d28d9"],["4","Facts","amount local, amount USD, count","#6d28d9"]])},
  {h:"A star: facts in the middle, descriptions around it",
   say:"The fact table holds numbers and keys. Each key points to a dimension that describes it. Questions become: filter dimensions, add up facts.",
   art: `<div class="star"><div class="c">fct_transactions<small>amount, count</small></div>
     <span style="top:2%;left:38%">dim_date</span><span style="top:22%;left:2%">dim_customer</span><span style="top:22%;right:2%">dim_account</span>
     <span style="bottom:22%;left:2%">dim_branch</span><span style="bottom:22%;right:2%">dim_currency</span><span style="bottom:2%;left:30%">dim_transaction_type</span></div>`},
  {h:"Same customer, two eras",
   say:"A March payment must stay MASS even after the August upgrade. So a customer has versions, each valid for a time window.",
   art: tbl(["customer_key","segment","valid_from","valid_to"],[["a91f…","MASS","1900-01-01","2026-08-12"],["c33b…","AFFLUENT","2026-08-12","9999-12-31"]]) +
        note("This is Slowly Changing Dimension type 2. The payment joins to the version whose window contains the payment time.")},
  {h:"Forget the time window and rows double",
   say:"Join a payment on customer_id alone and it matches every version. One payment becomes two. That bug is called fan-out.",
   art: pair("Wrong","on customer_id → 2 versions match → amount counted twice","Right","on customer_id and valid_from ≤ payment time &lt; valid_to → 1 match") +
        note("The macro scd2_match writes this condition for you. Lab 04 in E8 shows the explosion.")},
  {h:"Small patterns with names",
   say:"These words come up in every interview. Each one is in this project.",
   art: tbl(["Pattern","Here"],[
     ["Surrogate key","customer_key: a hash of customer_id and version start"],
     ["Unknown member","-1 rows, so a payment with no matching customer still joins"],
     ["Junk dimension","dim_transaction_type: type × status combinations"],
     ["Degenerate dimension","reference_no kept on the fact, no table of its own"],
     ["Bridge table","bridge_account_customer for joint accounts"],
     ["Conformed dimension","dim_customer shared by payments, cards, loans"]])},
  {h:"Three kinds of fact table",
   say:"A transaction is a receipt. A monthly balance is a photograph. A loan application is a story with milestones.",
   art: tbl(["Kind","Our table","One row"],[
     ["Transaction","fct_transactions, fct_card_authorizations","one event"],
     ["Periodic snapshot","fct_monthly_account_balance","one account per month end"],
     ["Accumulating snapshot","fct_loan_applications, fct_card_applications","one application, updated as it moves"]])},
  {h:"Money is converted on the day it moved",
   say:"Store the rupees, the dollars, and the rate used that day. History must not change when today's rate changes.",
   art: `<p class="big">₹2,400 × rate on that day = USD stored</p>` +
        note("Weekend days have no rate, so the last known rate is carried forward and flagged fx_is_forward_filled.")},
  {h:"The bus matrix",
   say:"Rows are business processes. Columns are dimensions. A tick means that process uses that dimension. Shared columns are what make reports join.",
   plain:["Open 07_data_modelling/BUS_MATRIX.md on camera.","Fill one row live: card authorizations uses date, customer, card, merchant, sale event."]},
  {k:"quiz", h:"Check yourself", qs:[
   ["What is fan-out?","A join that matches more than one row on the other side, so facts are counted more than once. In SCD2 it happens when the time window is missing."],
   ["Why valid_to = 9999-12-31 instead of NULL?","The range check stays simple: valid_from ≤ ts < valid_to always works."],
   ["Which fact type is fct_monthly_account_balance?","Periodic snapshot."]]}
 ]},

// ================================================================ E3
{id:"e3", code:"E3", mins:"40 min", color:"#0e7490", title:"Snowflake: rooms, keys, empty shelves",
 slides:[
  {h:"Storage and compute are separate",
   say:"Data sits in storage. A warehouse is just a computer you rent by the second to read it. Pause the computer and the data is still there.",
   art: `<div class="sfarch"><div>Cloud services<small>logins, query plans, policies</small></div><div class="row"><span>WH_INGEST_XS</span><span>WH_TRANSFORM_XS</span><span>WH_BI_XS</span></div><div>Storage<small>MERIDIAN_RAW · MERIDIAN_ANALYTICS</small></div></div>` +
        note("Separate warehouses per job: the loader cannot slow down dbt, and you can see who spent the credits.")},
  {h:"Roles: who may do what",
   say:"People and robots get roles. Roles get permissions. Nobody gets permissions directly.",
   art: tbl(["Role","Job"],[
     ["MERIDIAN_LOADER","PUT and COPY into MERIDIAN_RAW"],
     ["MERIDIAN_TRANSFORMER","dbt: reads raw, builds MERIDIAN_ANALYTICS"],
     ["MERIDIAN_ANALYST","reads MARTS"],["MERIDIAN_ML","reads gold, writes MERIDIAN_RAW.ML"],
     ["MERIDIAN_APP","owns the Streamlit app"],
     ["MERIDIAN_CEO, BRANCH_MANAGER, STAFF, CUSTOMER","the four people in the English demo"]])},
  {h:"Robots log in with a key, not a password",
   say:"The public key is a lock I give Snowflake. The private key stays on my laptop. Only my key opens that lock.",
   art: flow([["On your Mac","meridian_rsa_key.p8","private key: never share, never commit","#991b1b"],["In Snowflake","RSA_PUBLIC_KEY","the matching public key on each robot user","#0e7490"]]) +
        note("One key pair serves three robot users: MERIDIAN_LOADER_SVC, MERIDIAN_DBT_SVC, MERIDIAN_ML_SVC.")},
  {h:"What script 03 builds for bronze",
   say:"Each source table gets a raw table with four columns. The control schema keeps the courier's bookmarks and logs.",
   art: tbl(["Column","Meaning"],[
     ["record VARIANT","the whole source row as JSON-like data"],
     ["_extracted_at","when the courier read it"],
     ["_batch_id","which run carried it"],
     ["_source_file","which Parquet file it came from"]]) +
     note("Control tables: WATERMARKS (bookmark per table), LOAD_LOG (every batch), V_PIPELINE_HEALTH (how far behind each table is).")},
  {k:"do", h:"Give yourself the roles, then run script 01", where:"Snowsight · ACCOUNTADMIN",
   cmd:`Open ${ROOT}/03_snowflake/01_account_setup_rbac.sql
Paste into a Snowsight worksheet. Run all as ACCOUNTADMIN.

GRANT ROLE MERIDIAN_LOADER, MERIDIAN_TRANSFORMER, MERIDIAN_ANALYST, MERIDIAN_ML, MERIDIAN_APP TO USER DRIVEONE;`,
   happened:["Script 01 creates the roles, four warehouses, the robot users, and a monitor that stops spending.","The GRANT lets your own login switch into those roles."],
   see:"SHOW ROLES lists 9 MERIDIAN_ roles. SHOW WAREHOUSES lists 4 WH_ warehouses.",
   trap:"The GRANT is commented out in the file. Without it, script 03 fails on its first line, USE ROLE MERIDIAN_LOADER."},
  {k:"do", h:"Put the real public key on the three robots", where:"Terminal, then Snowsight · ACCOUNTADMIN",
   cmd:`grep -v "PUBLIC KEY" /Users/fakhruddinkhambaty/.ssh/meridian_rsa_key.pub | tr -d '\\n'

-- Snowsight. Replace PASTE with that one line, in all three:
ALTER USER MERIDIAN_LOADER_SVC SET RSA_PUBLIC_KEY = 'PASTE';
ALTER USER MERIDIAN_DBT_SVC SET RSA_PUBLIC_KEY = 'PASTE';
ALTER USER MERIDIAN_ML_SVC SET RSA_PUBLIC_KEY = 'PASTE';
DESC USER MERIDIAN_LOADER_SVC;`,
   happened:["grep removes the BEGIN and END lines. tr joins the rest into one line.","Each ALTER attaches the lock to one robot.","DESC shows a fingerprint when it worked."],
   see:"RSA_PUBLIC_KEY_FP has a value.",
   trap:"The sample text MIIBIjANBg… in the SQL file is not a key. Never paste the .p8 private key."},
  {k:"do", h:"Databases, then the empty raw tables", where:"Snowsight",
   cmd:`Open ${ROOT}/03_snowflake/02_databases_schemas_grants.sql
Run all.

Open ${ROOT}/03_snowflake/03_stages_raw_tables_control.sql
Run all. It switches to MERIDIAN_LOADER itself.`,
   happened:["02 creates MERIDIAN_RAW and MERIDIAN_ANALYTICS and their schemas, and grants each role its part.","03 creates the Parquet file format, the stages, the raw tables and the control tables."],
   see:"11 tables in POSTGRES_CORE, 8 in POSTGRES_REF, 1 in POSTGRES_CDC.",
   trap:"Skip 04_streams_tasks_dynamic_tables_demo.sql on the working path. Its task wakes every minute and spends credits."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why four warehouses and not one?","So one job cannot slow another, and cost can be traced to the job that spent it."],
   ["What happens to data when a warehouse suspends?","Nothing. Data lives in storage. Only the computer stops."],
   ["Which key does Snowflake hold?","The public key. The private key never leaves the laptop or the Airflow container."]]}
 ]},

// ================================================================ PYTHON FOUNDATIONS
{id:"py0", code:"P0", mins:"35 min", color:"#a16207", title:"Python foundations for this pipeline",
 slides:[
  {h:"Browser practice is not the project runtime",
   say:"Use a browser editor to learn one idea. Use local Python 3.12 for Meridian because it must reach Docker Postgres, local files and Snowflake.",
   art: pair("Programiz / Python Tutor","No installation. Good for print, if, loops and watching values change.",
            "Cursor + Terminal + .venv","The real project. Libraries, files, Docker databases, private keys and command-line flags.")},
  {k:"code", h:"Values, print, types and casting", file:"02_ingestion_python/00_python_foundations/01_values_and_decisions.py",
   lines:[
    [`source_rows_text = "100000"`,"Quotes make this text, exactly as an environment variable arrives"],
    [`source_rows = int(source_rows_text)`,"Cast the text to a number before doing arithmetic"],
    [`difference_ratio = abs(difference) / source_rows`,"Calculate how far the two systems disagree"],
    [`print("Reconciliation:", status)`,"Show the result to a person and to the task log"]]},
  {k:"code", h:"if decides; for and while repeat", file:"01_values_and_decisions.py + 02_loops_and_functions.py",
   lines:[
    [`if difference == 0: ... elif difference_ratio <= tolerance: ... else: ...`,"Exactly one branch runs"],
    [`for table in tables_to_load(...):`,"Do the same work once for every selected table"],
    [`while run_number <= 3:`,"Repeat while a condition stays true; the real loader uses this for --loop"],
    [`run_number += 1`,"Change the value, or a bounded while loop never ends"]]},
  {k:"code", h:"Functions make one job nameable", file:"02_loops_and_functions.py",
   lines:[
    [`def tables_to_load(all_tables, hot_only):`,"Inputs enter through the parentheses"],
    [`return [name for name in all_tables if ...]`,"return sends one answer back"],
    [`def main() -> None:`,"main is the readable starting point for the script"],
    [`if __name__ == "__main__": main()`,"Run main only when this file is executed, not when it is imported"]]},
  {h:"Collections and libraries",
   say:"A list is an ordered set of things. A dictionary maps a key to a value. An import borrows code from Python, this project or an installed library.",
   art: tbl(["Shape","Meridian example","Meaning"],[
     ["list","files = [part_1, part_2]","many Parquet files in order"],
     ["dictionary","settings = {'table': 'transactions'}","named values looked up by key"],
     ["standard library","from pathlib import Path","ships with Python"],
     ["third-party library","import pandas as pd","installed by pip from requirements.txt"],
     ["local module","from config import PG, SF","our own project file"]])},
  {k:"code", h:"Paths, arguments and exceptions", file:"03_collections_paths_libraries.py",
   lines:[
    [`project_root = Path(__file__).resolve().parents[2]`,"Find the project from the file, not from a fragile typed path"],
    [`parser.add_argument("--limit", type=int, default=3)`,"Turn a terminal flag into a typed value"],
    [`try: ... except (KeyError, TypeError) as exc:`,"Name expected failures and explain them"],
    [`finally: print(...)`,"Cleanup runs whether the work passed or failed"]]},
  {h:"The four data libraries, in one sentence each",
   say:"You do not need to memorise their APIs. Know the job each toolbox performs.",
   art: tbl(["Library","Job in Meridian"],[
     ["psycopg2","opens Postgres and streams source rows"],
     ["pandas","holds rows as a DataFrame and compares aggregates"],
     ["pyarrow","gives the DataFrame types and writes compressed Parquet"],
     ["snowflake-connector","logs in, uploads files, runs COPY and reads control tables"]])},
  {k:"do", h:"Run the bridge before the extractor", where:"Terminal · project root",
   cmd:`source .venv/bin/activate
python 02_ingestion_python/00_python_foundations/01_values_and_decisions.py
python 02_ingestion_python/00_python_foundations/02_loops_and_functions.py
python 02_ingestion_python/00_python_foundations/03_collections_paths_libraries.py --limit 2
python 02_ingestion_python/00_python_foundations/04_mini_reconciliation.py || true`,
   happened:["The first three scripts finish successfully.","The fourth deliberately finds two missing rows and exits 1; || true keeps this teaching command moving.","Now read config.py, then follow main() in pg_to_snowflake.py."],
   see:"FAILED is expected in the final example; it proves a mismatch becomes a machine-readable failure.",
   trap:"Browser editors cannot reach your local Postgres or Snowflake. Move to the local virtual environment before Module 4."}
 ]},

// ================================================================ E4
{id:"e4", code:"E4", mins:"40 min", color:"#1e4b7a", title:"Python carries only what changed",
 slides:[
  {h:"Why Python is needed at all",
   say:"dbt only sends SQL to Snowflake. Snowflake cannot reach the Postgres on my laptop. Something has to read Postgres and hand files to Snowflake. That is this script.",
   plain:["A 'Snowflake connector' is the login cable. It is not a job that copies data.",
          "Dynamic tables and incremental models refresh data that is already inside Snowflake.",
          "In production, Fivetran or Debezium does this job. We write it so you can see every step."]},
  {h:"The bookmark, called a watermark",
   say:"Each table has a bookmark: the newest updated_at already copied. Next run asks for rows after the bookmark and up to 10 seconds ago.",
   art: `<div class="wm"><div class="done">already copied</div><div class="win">this run's window</div><div class="lag">10 s</div><span class="mark">watermark</span><span class="hi">now − 10 s</span></div>` +
        note("The 10-second gap leaves room for payments that started but have not committed yet. They are picked up next run.")},
  {h:"One run for one table, in five steps",
   say:"Read, write files, upload, copy, move the bookmark. The bookmark moves last.",
   art: flow([["1","SELECT","rows in the window","#336791"],["2","Parquet","200,000 rows per file","#1e4b7a"],["3","PUT","upload to the stage","#0e7490"],["4","COPY","into the raw table","#0e7490"],["5","Watermark","to the newest row seen","#166534"]])},
  {k:"code", h:"Step 1–2: read Postgres, write Parquet", file:"02_ingestion_python/pg_to_snowflake.py · extract_table()",
   lines:[
    [`SELECT * FROM {table} WHERE {cursor} > %s AND {cursor} <= %s ORDER BY {cursor}`,"Only rows inside the window. %s are filled with the watermark and now − 10 s."],
    [`with pg_conn.cursor(name=...) as cur:`,"A named cursor streams rows from the server instead of loading 5 million into memory"],
    [`rows = cur.fetchmany(INGEST.chunk_rows)`,"Take 200,000 rows at a time"],
    [`df["_extracted_at"] = ...; df["_batch_id"] = batch_id`,"Stamp each row with when and which run"],
    [`max_cursor = max(max_cursor, chunk_max)`,"Remember the newest updated_at actually seen"],
    [`pq.write_table(arrow_table, path, compression="snappy")`,"One compressed Parquet file per chunk"]]},
  {k:"code", h:"Step 3–5: upload, copy, move the bookmark", file:"02_ingestion_python/pg_to_snowflake.py · load_files(), process_table()",
   lines:[
    [`PUT file://{pattern} {stage} AUTO_COMPRESS=FALSE PARALLEL=8`,"Upload all files of this run to a Snowflake stage, 8 at a time"],
    [`COPY INTO {target} (record, _extracted_at, _batch_id, _source_file)`,"Load staged files into the raw table"],
    [`SELECT $1, %s::TIMESTAMP_NTZ, %s, METADATA$FILENAME FROM {stage}`,"$1 is the whole Parquet row, which becomes record"],
    [`ON_ERROR = ABORT_STATEMENT  PURGE = TRUE`,"Any bad file fails the whole load. Delete staged files after success."],
    [`set_watermark(sf_cur, table, max_cursor, batch_id)`,"Only now, after COPY succeeded, move the bookmark to the newest row seen"]]},
  {h:"What if it crashes in the middle?",
   say:"If the script dies after COPY but before the bookmark moves, the next run copies the same rows again. Bronze gets duplicates. Silver keeps one. Nothing is lost.",
   art: pair("Crash before COPY","nothing loaded, bookmark unchanged → next run retries","Crash after COPY, before bookmark","rows loaded twice → staging keeps the newest copy") +
        note("This property is called idempotent: running it again gives the same final answer.")},
  {k:"do", h:"Confirm .env is a file, not a command", where:"Cursor",
   cmd:`Open ${ROOT}/.env

SNOWFLAKE_ACCOUNT=SJVOGGD-MQ92888
SNOWFLAKE_USER=MERIDIAN_LOADER_SVC
SNOWFLAKE_PRIVATE_KEY_PATH=/Users/fakhruddinkhambaty/.ssh/meridian_rsa_key.p8
SNOWFLAKE_ROLE=MERIDIAN_LOADER
SNOWFLAKE_WAREHOUSE=WH_INGEST_XS
SNOWFLAKE_RAW_DATABASE=MERIDIAN_RAW`,
   happened:["Python reads these settings from the file when it starts."],
   see:"The file exists with these values.",
   trap:"Do not paste these lines into Terminal. Press Cmd+P and type .env if the file is hidden."},
  {k:"do", h:"One tiny table, then everything", where:"Terminal",
   cmd:`${ENV}
python 02_ingestion_python/pg_to_snowflake.py --tables ref.currencies -v && time python 02_ingestion_python/pg_to_snowflake.py`,
   happened:["cd, then activate the Python environment so python exists.","set -a; source .env loads the settings into this terminal.","Load one 5-row table first. If it fails, it is the account, key or role, not the code.","&& runs the full load only if the small one worked."],
   see:"Currencies loads 5 rows. Then all 20 tables. About 25 Parquet files for transactions.",
   trap:"'python: command not found' means .venv is not active. 'No such file' means you are not in the project folder."},
  {k:"do", h:"Health, then the two counts", where:"Snowsight and DBeaver",
   cmd:`SELECT * FROM MERIDIAN_RAW.CONTROL.V_PIPELINE_HEALTH;
SELECT COUNT(*) FROM MERIDIAN_RAW.POSTGRES_CORE.TRANSACTIONS;
-- DBeaver, meridian_core:
SELECT count(*) FROM core.transactions;`,
   happened:["The health view shows each table's last load and minutes behind.","The two counts compare bronze with the bank."],
   see:"Loads are SUCCESS or NO_CHANGES. Counts are equal right after the first full load.",
   trap:"After the simulator runs, Snowflake shows more rows. That is bronze keeping every version. Compare after dbt, in E6."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why move the watermark to the newest row seen, not to 'now − 10 s'?","If the table had no new rows, the bookmark stays put. Moving it to the clock could skip rows that commit late."],
   ["Why the 10-second lag?","A transaction that started earlier may commit after this run's read. The gap gives it time."],
   ["Does the loader see deletes?","Not in the table itself. It copies cdc.deleted_records like any table; dbt applies the deletes."]]}
 ]},

// ================================================================ E5
{id:"e5", code:"E5", mins:"45 min", color:"#c2410c", title:"dbt cleans the inbox",
 slides:[
  {h:"What dbt actually is",
   say:"dbt turns SELECT statements into tables and views inside Snowflake, in the right order. It works out the order from ref().",
   art: flow([["You write","SELECT …","with ref() and source()","#c2410c"],["dbt compiles","plain SQL","for Snowflake","#c2410c"],["Snowflake runs","CREATE TABLE AS","on its warehouse","#0e7490"]]) +
        note("dbt never touches Postgres. It only reads bronze, which the courier already loaded.")},
  {h:"Folders map to layers",
   say:"models/staging is silver. models/intermediate is silver logic. models/marts is gold. snapshots record history.",
   art: tbl(["Folder","Count","Becomes","Layer"],[
     ["models/staging","21 models","views, transactions is incremental","Silver"],
     ["snapshots","3","SCD2 history tables","Silver"],
     ["models/intermediate","3","views","Silver"],
     ["models/marts","27","tables, some incremental","Gold"],
     ["tests, unit tests","137 data, 3 unit, 6 singular","checks after each build","—"]])},
  {k:"code", h:"Staging: VARIANT to typed columns, newest copy only", file:"models/staging/postgres/stg_postgres__transactions.sql",
   lines:[
    [`materialized='incremental', unique_key='transaction_id'`,"First run builds the table. Later runs only MERGE new rows into it."],
    [`from {{ source('postgres_core', 'transactions') }}`,"Read bronze: MERIDIAN_RAW.POSTGRES_CORE.TRANSACTIONS"],
    [`and _extracted_at > (select dateadd('hour', -2, max(_extracted_at)) from {{ this }})`,"Only rows loaded since last time, minus a 2-hour safety overlap"],
    [`record:transaction_id::number as transaction_id`,"Pull a field out of the JSON and give it a type"],
    [`record:amount::number(18,2) as amount`,"Money as an exact decimal, never a float"],
    [`qualify row_number() over (partition by transaction_id order by updated_at desc, _extracted_at desc) = 1`,"Several copies of one payment: keep the newest"],
    [`post_hook = apply_hard_deletes('transactions', 'transaction_id')`,"After the merge, delete ids found in the delete log"]]},
  {h:"Incremental, first run and every run after",
   say:"The first build reads all of bronze. Every later build reads only the last couple of hours of arrivals and merges them in by id.",
   art: pair("First run","5.3 million rows read, table created","Later runs","only new arrivals; MERGE updates PENDING to POSTED in place") +
        note("dbt prints SUCCESS 1 for a table creation. That is a statement count, not the number of rows.")},
  {h:"Snapshots: a camera on a table",
   say:"Each run, the snapshot compares customers with its last picture. If updated_at moved, it closes the old row and opens a new one.",
   art: tbl(["customer_id","segment","dbt_valid_from","dbt_valid_to"],[["4821","MASS","09:00","10:15"],["4821","AFFLUENT","10:15","(open)"]]) +
        note("strategy='timestamp' relies on updated_at, which the Postgres trigger guarantees. Snapshots run in the daily DAG.")},
  {k:"code", h:"Dev and prod never collide", file:"macros/generate_schema_name.sql",
   lines:[
    [`{%- if custom_schema_name is none -%}`,"A model with no schema setting uses the default"],
    [`{%- elif target.name in ['prod', 'dev_clone'] -%}  {{ custom_schema_name }}`,"In prod: STAGING, INTERMEDIATE, MARTS"],
    [`{%- else -%}  {{ default_schema }}_{{ custom_schema_name }}`,"In dev: DBT_FK_STAGING, DBT_FK_MARTS"]]},
  {h:"Dev builds only 30 days",
   say:"limit_in_dev adds a date filter when the target is not prod. Fast, cheap practice. Unit tests skip it, because their fake rows have fixed dates.",
   plain:["We hit this: a unit test with September rows returned nothing because the 30-day filter removed them. The macro now skips unit tests."]},
  {k:"do", h:"Load settings, connect, install packages, build dev", where:"Terminal",
   cmd:`${DBT}
cp -n profiles.yml.example profiles.yml
dbt debug --target dev
dbt debug --target prod
dbt deps
time dbt build --target dev`,
   happened:["The first lines load .env into the shell. dbt reads only the shell, not the file.","cd 04_dbt_meridian_dw: dbt only works next to dbt_project.yml.","cp -n makes profiles.yml once and never overwrites it.","debug tests both logins. deps installs dbt_utils and dbt_expectations.","build runs models, snapshots, seeds and tests in dependency order."],
   see:"All checks passed twice. Build ends with ERROR=0. New schemas DBT_FK_STAGING, DBT_FK_MARTS.",
   trap:"'Env var SNOWFLAKE_ACCOUNT not set' means the set -a line was skipped in this terminal."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why is only transactions incremental in staging?","It grows by millions of rows. Re-reading all of it every 5 minutes would waste credits. Small tables are views."],
   ["What does the 2-hour lookback protect against?","A run that overlapped a COPY or failed after merge. The rows are seen again and unique_key makes that harmless."],
   ["Where do dev models land?","DBT_FK_* schemas, because target is not prod."]]}
 ]},

// ================================================================ E6
{id:"e6", code:"E6", mins:"50 min", color:"#c2410c", title:"The star schema, for real",
 slides:[
  {h:"The build order dbt worked out",
   say:"Staging feeds intermediate. Snapshots feed dimensions. Dimensions and intermediate feed the fact.",
   art: flow([["Silver","stg_postgres__transactions","newest copy","#94a3b8"],["Silver","int_transactions_with_fx","USD and primary holder","#94a3b8"],["Gold","dim_customer, dim_account","from snapshots","#ca8a04"],["Gold","fct_transactions","joins all of them","#ca8a04"]])},
  {k:"code", h:"Intermediate: convert at the day's rate", file:"models/intermediate/int_transactions_with_fx.sql",
   lines:[
    [`left join holders h on h.account_id = t.account_id`,"Find the primary customer of the account"],
    [`left join fx on fx.date_day = t.transaction_date and fx.currency_code = t.currency_code`,"The rate on the payment's own date"],
    [`round(t.amount * fx.rate_to_reporting, 2) as amount_reporting`,"USD amount, stored, not calculated at query time"],
    [`iff(is_credit, t.amount, -t.amount) as signed_amount_local`,"Money in is positive, money out is negative"]]},
  {k:"code", h:"dim_customer: versions from the snapshot", file:"models/marts/core/dim_customer.sql",
   lines:[
    [`generate_surrogate_key(['customer_id', 'dbt_valid_from']) as customer_key`,"One key per version"],
    [`first version: valid_from = 1900-01-01`,"Backdating: payments older than the first snapshot still find a version"],
    [`open version: valid_to = 9999-12-31`,"Never NULL, so range checks stay simple"],
    [`unknown member customer_key = '-1'`,"A row for 'no customer found', so joins never drop payments"]]},
  {k:"code", h:"fct_transactions: the fact", file:"models/marts/core/fct_transactions.sql",
   lines:[
    [`-- depends_on: {{ ref('stg_postgres__deleted_records') }}`,"Tells dbt about a ref hidden inside the delete macro. We hit this error in the prod build."],
    [`merge_exclude_columns=['inserted_at']`,"On update, keep the original insert time"],
    [`left join dim_customer dc on dc.customer_id = t.primary_customer_id and {{ scd2_match('t.transaction_ts', 'dc') }}`,"Point-in-time join: the version valid when they paid"],
    [`coalesce(dc.customer_key, '-1') as customer_key`,"No match falls to the unknown member"],
    [`1 as transaction_count`,"A count measure, so 'how many' is a SUM like every other measure"],
    [`current_timestamp()::timestamp_ntz as inserted_at`,"Cast to NTZ: the contract says timestamp_ntz. Bare current_timestamp() is LTZ and failed the build."],
    [`meta={'governance': {'row_access': {'policy': 'RAP_CUSTOMER_SCOPE'}}}`,"After build, a hook re-attaches the row policy on customer_id"]]},
  {h:"Deletes need their own step",
   say:"MERGE only touches rows in the new batch. A deleted payment never arrives, so MERGE never sees it. The post-hook deletes ids found in the delete log.",
   art: pair("MERGE alone","deleted payment stays in gold forever","MERGE + apply_hard_deletes","ids in cdc.deleted_records are removed after each run")},
  {h:"Four kinds of test",
   say:"Data tests check the rows. Unit tests check logic on rows I wrote by hand. Contracts check the shape. Singular tests check a business rule.",
   art: tbl(["Kind","Example here"],[
     ["Data test","transaction_id unique and not null; amount > 0"],
     ["Unit test","a PENDING then POSTED payment comes out as one POSTED row"],
     ["Contract","fct_transactions must have these columns with these types"],
     ["Singular test","assert_fct_transactions_reconciles_to_staging: counts and amounts match"]])},
  {h:"Three errors from our own prod build",
   say:"These are the stories to tell. Each one teaches how dbt works.",
   art: tbl(["Error","Cause","Fix"],[
     ["ref inside a conditional","the delete macro's ref is inside is_incremental()","-- depends_on comment at the top of the model"],
     ["Contract: LTZ vs NTZ","current_timestamp() returns local-time-zone timestamps","::timestamp_ntz"],
     ["search_text search_text =","expression_is_true already puts the column name first","start the expression with ="]])},
  {k:"do", h:"Production build, then reconcile", where:"Terminal",
   cmd:`${DBT}
time dbt build --target prod

cd ${ROOT}
python 02_ingestion_python/reconcile_with_pandas.py --days 7`,
   happened:["Builds everything into the real STAGING, INTERMEDIATE, MARTS schemas.","Reconcile counts payments per day and currency in Postgres and in fct_transactions, and compares."],
   see:"PASS=196 ERROR=0. Reconcile reports zero mismatched groups after applying the same two-minute cutoff to both systems.",
   trap:"A governance warning is expected until E11. Reconcile runs from the project folder, not from 04_dbt_meridian_dw."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why does fct_transactions keep customer_id as well as customer_key?","customer_id is for reconciliation and the row policy. customer_key is for the historical join."],
   ["What would happen without scd2_match?","Every customer version would match. Amounts would double for customers who changed."],
   ["Why a post-hook for deletes?","MERGE cannot delete a row that is not in the incoming batch."]]}
 ]},

// ================================================================ E7
{id:"e7", code:"E7", mins:"30 min", color:"#1d4ed8", title:"Airflow is the alarm clock",
 slides:[
  {wide:true, h:"Airflow runs commands you already ran by hand",
   say:"Airflow transforms nothing. It runs the Python loader and dbt on a timer, in order, with retries, and shows what happened.",
   art: tbl(["DAG","When","Does"],[
     ["meridian_microbatch_ingest","every 5 min","4 hot tables → dbt build --selector microbatch → health check"],
     ["meridian_daily_batch","02:00 UTC","all 17 tables → snapshots → full build → reconcile → docs → save manifest"],
     ["meridian_source_freshness","every 15 min","alarms if the 5-minute DAG stopped"],
     ["meridian_card_decisioning","Mondays 03:00 UTC","train and publish card scores"],
     ["meridian_bounded_replay","manual","re-copy one time window after an incident"]])},
  {wide:true, h:"The 5-minute DAG",
   say:"Four extracts in parallel, then dbt, then a health gate that fails if any hot table is more than 15 minutes behind.",
   art: `<div class="dag"><div class="col"><span>transactions</span><span>card_applications</span><span>card_authorizations</span><span>deleted_records</span></div><i>→</i><div class="col"><span>dbt_build_hot_path</span></div><i>→</i><div class="col"><span>report_pipeline_health</span></div></div>`},
  {k:"code", h:"The DAG file", file:"05_airflow/dags/meridian_microbatch_ingest.py",
   lines:[
    [`schedule="*/5 * * * *"`,"Every 5 minutes"],
    [`catchup=False`,"Do not replay missed intervals. The watermark already knows where we are."],
    [`max_active_runs=1`,"A slow run never overlaps the next; two runs would race on the watermark"],
    [`@task.bash(pool=INGEST_POOL, max_active_tis_per_dag=4)`,"At most 4 reads on Postgres at once, so the bank stays fast"],
    [`return f"cd {INGEST_DIR} && python pg_to_snowflake.py --tables {table}"`,"The same command you ran in E4"],
    [`extract_load.expand(table=HOT_TABLES)`,"One task per table: separate logs and retries"],
    [`@task.bash(trigger_rule="all_done")`,"Health check runs even if something failed, so it can report it"]]},
  {wide:true, h:"Containers see different paths",
   say:"Airflow runs in Docker. Inside a container, localhost is the container, and ~/.ssh does not exist. So it gets its own copy of the code, key and .env.",
   art: tbl(["Setting","Your Mac's .env","05_airflow/.env"],[
     ["PG_HOST","localhost","host.docker.internal"],
     ["SNOWFLAKE_PRIVATE_KEY_PATH","/Users/…/.ssh/meridian_rsa_key.p8","/usr/local/airflow/include/keys/meridian_rsa_key.p8"]]) +
     note("include/ is a copy. When you change a script in the project, copy it into include/ again.")},
  {h:"The pool, and the run that looked stuck",
   say:"Tasks asked for a pool called meridian_postgres that did not exist. Airflow waited politely forever. The run said running; nothing ran.",
   art: pair("Without the pool","tasks stay scheduled, DAG shows running for hours","After astro dev object import","4 slots exist, extracts finish in seconds")},
  {k:"do", h:"Copy the project into the container's folder", where:"Terminal · 05_airflow",
   cmd:`cd ${ROOT}/05_airflow
mkdir -p include/keys .astro
cp -R ../04_dbt_meridian_dw include/dbt
cp -R ../02_ingestion_python include/ingestion
cp -R ../09_decisioning_python include/decisioning
cp /Users/fakhruddinkhambaty/.ssh/meridian_rsa_key.p8 include/keys/
cp ../.env .env
sed -i '' -e 's#^PG_HOST=.*#PG_HOST=host.docker.internal#' -e 's#^SNOWFLAKE_PRIVATE_KEY_PATH=.*#SNOWFLAKE_PRIVATE_KEY_PATH=/usr/local/airflow/include/keys/meridian_rsa_key.p8#' .env
cp airflow_settings.yaml.example airflow_settings.yaml
test -f .astro/config.yaml || printf 'project:\\n    name: meridian\\n' > .astro/config.yaml
grep -E '^(PG_HOST|SNOWFLAKE_PRIVATE_KEY_PATH)=' .env`,
   happened:["Copies dbt, loader and scoring code into include/, which the containers can see.","Copies the key and .env, then sed rewrites the two lines for the container.","The .astro marker tells the astro CLI this folder is an Airflow project.","grep shows the two rewritten lines."],
   see:"PG_HOST=host.docker.internal and the /usr/local/airflow key path.",
   trap:"Never run astro dev init here: it overwrites the Dockerfile and DAGs. Copy after dbt deps, so packages come along."},
  {k:"do", h:"Start Airflow, then create the pool", where:"Terminal · 05_airflow",
   cmd:`cd ${ROOT}/05_airflow
astro dev start
astro dev object import`,
   happened:["start builds the image and starts the scheduler, workers, UI and metadata database.","object import reads airflow_settings.yaml and creates the 4-slot pool."],
   see:"The CLI prints a URL. Open that. Five meridian_ DAGs, no import errors.",
   trap:"Port 8080 on this Mac belongs to another Airflow. Open the printed URL. If a DAG file is missing from the list, its first line must contain 'airflow' and 'DAG'."},
  {k:"do", h:"One 5-minute run, then one daily run", where:"Airflow UI",
   cmd:`Unpause meridian_microbatch_ingest. Wait for one green run.
Trigger meridian_daily_batch once.`,
   happened:["Unpausing lets the scheduler start the next 5-minute slot.","Trigger runs the daily chain now instead of at 02:00 UTC."],
   see:"Every task box green.",
   trap:"If reconcile fails only on the oldest day, the Postgres and Snowflake windows differ. The fixed script compares whole UTC dates."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why max_active_runs=1?","Two runs at once would read the same watermark and race to move it."],
   ["Why does the container's .env differ?","Inside Docker, localhost is the container and ~/.ssh does not exist."],
   ["A DAG says running for 20 minutes and nothing moves. First thing to check?","The task state. 'Scheduled' with a pool warning means the pool is missing."]]}
 ]},

// ================================================================ E8
{id:"e8", code:"E8", mins:"45 min", color:"#b45309", title:"Break it, measure, fix, measure",
 slides:[
  {h:"Every lab has four beats",
   say:"Break it. Measure. Change one thing. Measure again. Two numbers on screen, side by side.",
   art: flow([["1","Break","the naive query","#b45309"],["2","Measure","00_measure.sql reads QUERY_HISTORY","#b45309"],["3","Fix","one change only","#166534"],["4","Measure","same tag with _after","#166534"]])},
  {h:"Postgres reads every row",
   say:"The courier asks for rows by updated_at. Without an index, Postgres reads the whole table to find them.",
   art: pair("Before","Seq Scan, seconds","After","Index Scan on updated_at, milliseconds") + note(`DBeaver: ${ROOT}/06_performance_lab/01_postgres_missing_index.sql. Read EXPLAIN (ANALYZE, BUFFERS).`)},
  {h:"Snowflake opens files it doesn't need",
   say:"Snowflake stores tables in small blocks called micro-partitions. Random load order means every block holds every date, so a date filter opens them all.",
   art: pair("Random order","partitions scanned ≈ partitions total","Ordered or clustered by date","partitions scanned ≪ total") + note("02_snowflake_pruning_clustering.sql builds 100 million rows. Record it beforehand. Drop MERIDIAN_RAW.PERF_LAB afterwards.")},
  {h:"A sort spills to disk",
   say:"When a sort does not fit in memory, Snowflake writes to disk. Rewrite the query first. A bigger warehouse is the second experiment.",
   art: note("03_spilling_and_warehouse_size.sql. The number that moves: bytes spilled to local and remote storage.")},
  {h:"Fan-out looks like slowness",
   say:"Join payments to every customer version and the row count explodes. The fix is the date condition, not more compute.",
   art: pair("Without scd2_match","rows multiplied","With it","one row per payment") + note("04_join_explosion_scd2.sql")},
  {h:"The second run is a liar",
   say:"Snowflake caches results. Turn that off before claiming a query got faster.",
   art: pre(`ALTER SESSION SET USE_CACHED_RESULT = FALSE;`) + note("05_caching_layers.sql. Also 06 (filters that block pruning), 07 (search optimisation), 08 (incremental vs full refresh), 09 (warehouse size vs multi-cluster).")},
  {k:"quiz", h:"Check yourself", qs:[
   ["Why does wrapping a timestamp in TO_DATE() in a filter slow a query?","It can stop pruning. Filter on a range of the raw column instead."],
   ["What two numbers prove pruning worked?","partitions_scanned and partitions_total from the query profile."]]}
 ]},

// ================================================================ E9
{id:"e9", code:"E9", mins:"30 min", color:"#166534", title:"Quality, CI, cost, runbook",
 slides:[
  {h:"Green build is the first check, not the last",
   say:"Tests check rows. Reconciliation checks the bank against the warehouse. The health gate checks freshness. Cost views check who spent what.",
   art: tbl(["Check","Where"],[
     ["137 data tests, 3 unit tests","every dbt build"],
     ["Reconciliation by day and currency","daily DAG, written to CONTROL.RECONCILIATION_RUNS"],
     ["Freshness under 15 minutes","report_pipeline_health in the 5-minute DAG"],
     ["Credits per warehouse and query tag","03_snowflake/08_cost_attribution.sql"]])},
  {wide:true, h:"Reconciliation asks both systems the same question",
   say:"A dbt test can prove a fact has unique keys. Only a cross-system check can prove the source rows and amounts survived the journey.",
   art: tbl(["Step","Postgres","Snowflake","Why"],[
     ["Same cutoff","updated_at no newer than 2 minutes ago","completed warehouse data","do not call expected pipeline lag a loss"],
     ["Same grain","UTC date + currency or branch","date + currency or branch","compare like with like"],
     ["Same measures","row count + POSTED local amount","row count + POSTED local amount","keys alone do not prove money"],
     ["Outer merge","source-only groups stay visible","warehouse-only groups stay visible","an inner join would hide the worst failure"],
     ["Gate","0 mismatched groups","amount difference under one cent","record PASSED/FAILED; exit 0/1"]]) +
     note("Freshness = when did data arrive? Test = does one warehouse table obey a rule? Reconciliation = did the journey change business truth?")},
  {h:"CI builds only what changed",
   say:"On a pull request, CI compares my code with the production manifest and builds only changed models and what depends on them.",
   art: flow([["PR opened","GitHub Actions","meridian-dbt-ci.yml","#166534"],["Compare","state:modified+","with the saved prod manifest","#166534"],["Build","changed models","in a CI schema","#166534"]]) +
        note("The daily DAG's last task, dbt_save_prod_manifest, is what CI compares against.")},
  {h:"The runbook",
   say:"When something breaks at 2 a.m., the runbook says what to check, what bad looks like, and what to do.",
   plain:["Open 00_architecture/OPERATIONS_RUNBOOK.md on camera. Read one incident: a stale hot table.",
          "Then show meridian_bounded_replay: re-copy one time window without moving the watermark."]}
 ]},

// ================================================================ E10
{id:"e10", code:"E10", mins:"40 min", color:"#b45309", title:"Cards: score, then offer",
 slides:[
  {h:"Where the model sits",
   say:"Features come from gold. Python trains and scores. Scores land in bronze. dbt brings them into gold. Nothing writes back to the bank.",
   art: flow([["Gold","ml_customer_features","and card facts","#ca8a04"],["Python","train_and_score.py","scikit-learn","#1e4b7a"],["Bronze","RAW.ML.MODEL_SCORES","with MODEL_RUNS","#a16207"],["Gold","fct_next_best_offer","dbt","#ca8a04"]])},
  {h:"A model must pass a gate",
   say:"Each model is tested on the most recent days it never saw. Below 0.70 AUC, the run is REJECTED and no scores are written. The offer list falls back to rules.",
   art: pair("AUC below 0.70","REJECTED · score_source = RULE","AUC 0.70 or above","SUCCEEDED · score_source = MODEL") +
        note("AUC: the chance the model ranks a random positive above a random negative. 0.5 is a coin toss.")},
  {h:"Four models",
   art: tbl(["Model","Predicts","One row per"],[
     ["card_decision_v1","approve this application","application"],
     ["card_propensity_v1","would be approved if they applied","customer"],
     ["card_fraud_v1","this authorization is an injected fraud pattern","authorization"],
     ["card_fraud_customer_v1","highest recent fraud score","customer"]]),
   say:"Decide, target, protect. The fraud score also stops an offer going to someone under suspicion."},
  {k:"do", h:"Train, publish, then check the offers", where:"Terminal, then Snowsight",
   cmd:`${ENV}
python 09_decisioning_python/train_and_score.py
cd 04_dbt_meridian_dw
dbt build -s stg_ml__model_scores+ --target prod

SELECT score_source, COUNT(*)
FROM MERIDIAN_ANALYTICS.MARTS.FCT_NEXT_BEST_OFFER
GROUP BY 1;`,
   happened:["The script logs in as MERIDIAN_ML_SVC, trains, checks the gate, writes runs and scores.","stg_ml__model_scores+ builds the scores model and everything downstream of it."],
   see:"MODEL_RUNS has SUCCEEDED rows. The offer query has a MODEL row.",
   trap:"A login failure means SNOWFLAKE_ML_USER is missing from .env or the public key is not on MERIDIAN_ML_SVC."}
 ]},

// ================================================================ E11
{id:"e11", code:"E11", mins:"45 min", color:"#6d28d9", title:"Ask in English",
 slides:[
  {wide:true, h:"What happens when someone types a question",
   say:"The model writes SQL. Snowflake runs it as the signed-in person. The row policy decides which rows come back. The model never sees rows it isn't allowed to.",
   art: `<div class="seq"><span>Person types</span><i>→</i><span>Streamlit app</span><i>→</i><span>Cortex Analyst</span><i>→</i><span>SQL from the semantic view</span><i>→</i><span>Warehouse runs it as that user</span><i>→</i><span>Row policy filters</span><i>→</i><span>Table and SQL shown</span></div>`},
  {k:"code", h:"The semantic view is the menu", file:"10_semantic_app/01_semantic_view.sql",
   lines:[
    [`TABLES ( transactions AS MERIDIAN_ANALYTICS.MARTS.FCT_TRANSACTIONS ...`,"Only gold tables, with friendly names and synonyms like 'payments'"],
    [`RELATIONSHIPS ( transactions (customer_id) REFERENCES customers ...`,"Which joins are allowed"],
    [`DIMENSIONS ( customers.segment ... branches.city ...`,"Things you can group or filter by"],
    [`METRICS ( suspected_fraud_count AS COUNT(CASE WHEN is_rule_suspect THEN 1 END)`,"Named calculations, defined once"],
    [`AI_SQL_GENERATION 'Default transactions to status = POSTED ...'`,"House rules for the model"],
    [`AI_VERIFIED_QUERIES ( ... QUESTION ... SQL ...`,"Questions a human already checked"]]},
  {h:"Four people, same question, different rows",
   say:"Same SQL, same tables. Only who is signed in changes.",
   art: tbl(["Signed in as","Sees"],[
     ["MERIDIAN_CEO","every row"],["MERIDIAN_BM_MUMBAI","customers of branch IN-MUM-0001"],
     ["MERIDIAN_STAFF_MUMBAI","the same rows, email and phone masked"],["MERIDIAN_CUSTOMER","only their own rows"]])},
  {k:"code", h:"The row policy, in plain words", file:"03_snowflake/06_row_level_security.sql · RAP_CUSTOMER_SCOPE",
   lines:[
    [`WHEN EXISTS (... u.snowflake_user = CURRENT_USER() AND u.persona = 'CEO') THEN TRUE`,"CEO: every row"],
    [`WHEN EXISTS (... persona = 'CUSTOMER' AND u.customer_id = p_customer_id) THEN TRUE`,"Customer: only their own id"],
    [`WHEN EXISTS (... ENT_CUSTOMER_BRANCH b WHERE b.branch_id = (SELECT MIN(u.branch_id) ...))`,"Manager and staff: customers of their branch"],
    [`WHEN EXISTS (... u.snowflake_user = CURRENT_USER()) THEN FALSE`,"Any other app user: nothing"],
    [`ELSE IS_ROLE_IN_SESSION('MERIDIAN_TRANSFORMER') OR ...`,"Engineers and analysts outside the app see everything"]]},
  {h:"Why the policy has no JOIN",
   say:"Snowflake refuses a JOIN inside a row policy. Ours had one, and the app said 'Unsupported subquery type'. Rewritten as separate EXISTS checks, it works.",
   plain:["CURRENT_USER, not CURRENT_ROLE: the app identifies the person, not the role.",
          "CREATE IF NOT EXISTS does not change a policy that already exists. The script now ends with ALTER … SET BODY."]},
  {k:"do", h:"Policies, attach them, create the menu", where:"Snowsight, then Terminal",
   cmd:`-- Snowsight, ACCOUNTADMIN. Open and run all of:
${ROOT}/03_snowflake/06_row_level_security.sql

${DBT}
dbt run-operation apply_governance_all --target prod

-- Snowsight, MERIDIAN_TRANSFORMER. Open and run all of:
${ROOT}/10_semantic_app/01_semantic_view.sql`,
   happened:["Security creates policies, masks, the four users and who-is-who.","dbt attaches each policy to the gold tables that declare it.","The semantic view is created on MARTS."],
   see:"Four users mapped to IN-MUM-0001. SV_MERIDIAN_BANK exists.",
   trap:"Policies attach only after the tables exist, so this follows the prod build."},
  {k:"do", h:"Allow Cortex, set a password, ask", where:"Snowsight · ACCOUNTADMIN, then Terminal",
   cmd:`USE ROLE ACCOUNTADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MERIDIAN_CEO;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MERIDIAN_BRANCH_MANAGER;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MERIDIAN_STAFF;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MERIDIAN_CUSTOMER;
ALTER USER MERIDIAN_CEO SET PASSWORD = 'choose-a-password' MUST_CHANGE_PASSWORD = FALSE;

${ENV}
python -c "import streamlit" || pip install 'streamlit>=1.39'
streamlit run 10_semantic_app/streamlit_app.py`,
   happened:["CORTEX_USER lets each persona call the English-to-SQL service.","The password lets the app sign in as the CEO.","streamlit run opens the app at localhost:8501."],
   see:"Sign in as MERIDIAN_CEO. Click the fraud question. A count and its SQL come back.",
   trap:"Replace choose-a-password and never commit it. If the region lacks Cortex Analyst, use 04_dbt_meridian_dw/analyses/card_questions.sql."},
  {k:"quiz", h:"Check yourself", qs:[
   ["Who hides the rows: the model or Snowflake?","Snowflake, through the row policy, based on who is signed in."],
   ["Why a semantic view instead of letting the model read any table?","It limits the model to checked tables, joins and metrics, so the SQL is predictable."],
   ["Why CURRENT_USER in the policy?","The app may run as one role for everyone. The user name identifies the person."]]}
 ]},

// ================================================================ E12
{id:"e12", code:"E12", mins:"45 min", color:"#44403c", title:"The rules survive a rebuild",
 slides:[
  {h:"One owner per kind of object",
   say:"Security writes policies. dbt re-attaches them after every rebuild. An engineer can hang the lock on the door; only security changes what the lock allows.",
   art: tbl(["Owner","Owns"],[["Loader","MERIDIAN_RAW tables"],["dbt","tables in MERIDIAN_ANALYTICS"],["Security","policies, tags, APP_USER"],["Terraform","warehouses, roles, databases"]])},
  {h:"A contract that breaks the build",
   say:"dim_branch lists every column and type. Rename one column, build, read the refusal, rename it back.",
   art: pre(`${DBT}\ndbt build -s dim_branch --target dev`) + note("11_platform_terraform/main.tf describes the platform. terraform plan shows a change; apply only if you mean it.")},
  {h:"Prove who read what",
   say:"ACCESS_HISTORY records which user read which columns. That is the audit answer.",
   plain:["Show one query against SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY for MERIDIAN_CEO after the E11 demo. It can lag by up to a few hours."]}
 ]},

// ================================================================ E13
{id:"e13", code:"E13", mins:"20 min", color:"#166534", title:"Say it in two minutes",
 slides:[
  {h:"The pitch",
   say:"Watermark CDC from Postgres into an append-only bronze layer in Snowflake. dbt builds silver and a Kimball star in gold, with customer history and FX on the payment date. Airflow runs the hot path every five minutes and the heavy path nightly, with reconciliation. Models publish only if they pass a holdout gate. An English question becomes SQL against a semantic view, and a row policy keyed on the person decides what comes back.",
   art: flow([["Bronze","raw","every copy","#a16207"],["Silver","staging","one clean row","#94a3b8"],["Gold","marts","star schema","#ca8a04"],["Serve","English","policy-filtered","#6d28d9"]])},
  {h:"Tell one failure you fixed",
   say:"The failure is the proof that you built it.",
   art: tbl(["Story","Lesson"],[
     ["A DAG 'running' for 20 minutes doing nothing","a missing pool; read task state, not DAG state"],
     ["Raw had more rows than Postgres","bronze keeps every version by design"],
     ["Reconcile failed on one day only","the two systems used different date windows"],
     ["The app: Unsupported subquery type","no JOIN inside a row policy"]])}
 ]}
];

# Free-Tier Platform Comparison for a Notion + Python Project Dashboard

> **Goal:** A Notion projects table is the source of truth. A Python
> backend synchronizes it into a persistent database. A website reads
> from that database. Synchronization can be triggered manually or run
> daily.
>
> **Cost target:** ₱0, using free tiers where possible. Free-tier limits
> and terms can change, so verify them before deployment.

## 1. Python Backend Hosting Platforms

These providers can run FastAPI, Flask, Django, or other Python
applications.

### A. Traditional Python Hosting

These run an application as a web service rather than creating a
separate function for every request.

## Traditional Python Hosting Platforms

| Platform | Free-Tier Offering | Specific Limitations | Official Sources |
|---|---|---|---|
| **Render** | Free Python web services (FastAPI, Flask, Django) | Sleeps after 15 minutes without inbound traffic. Takes approximately one minute to wake. 750 free instance-hours/month. Filesystem is ephemeral; no persistent disks on free services. | [Free Services](https://render.com/docs/free) |
| **Koyeb** | One free web-service instance per organization | 0.1 vCPU, 512 MB RAM, 2 GB SSD. Limited to Frankfurt and Washington, D.C. Scales to zero after one hour without traffic. No persistent volumes. | [Pricing FAQ](https://www.koyeb.com/docs/faqs/pricing) · [Instance Types](https://www.koyeb.com/docs/reference/instances) |
| **PythonAnywhere** | One free Python web app, two consoles, 512 MB storage | Restricted outbound internet access. 100 CPU-seconds/day for consoles and scheduled/always-on tasks. No scheduled tasks for newly created Beginner accounts. | [Pricing](https://www.pythonanywhere.com/pricing/) · [Internet Access](https://help.pythonanywhere.com/pages/WhatIsTheInternet/) |
| **Oracle Cloud Infrastructure** | Always Free compute: up to two E2.1.Micro VMs or eligible Ampere A1 resources (up to 2 OCPUs and 12 GB RAM) | Requires manual server administration. Capacity is not guaranteed. Resources must be provisioned in your home region. Idle instances may be reclaimed under Oracle's policy. | [Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) |
| **Hugging Face Spaces** | Free Static Spaces; eligible accounts can use up to two ZeroGPU Spaces | Ordinary CPU-backed Gradio and Docker Spaces require paid hardware for personal accounts. Static Spaces cannot run a Python backend. Primarily designed for demos and interactive ML applications. | [Spaces Overview](https://huggingface.co/docs/hub/spaces-overview) |


## Evaluation Traditional Backend for the Notion Project Dashboard

## 1. Project Requirements

The dashboard uses Notion as its source of truth. A Python backend synchronizes Notion project records into a persistent database, and a website reads from that database.

The hosting platform should support:

- Conventional Python applications, preferably FastAPI.
- Outbound HTTPS requests to the Notion API.
- Connections to an external PostgreSQL database such as Neon.
- HTTP endpoints for manually triggered synchronization.
- Daily synchronization through an external scheduler if necessary.
- A target operating cost of **₱0**, subject to free-tier limits and provider policies.

---

## 2. Platform Evaluation

### A. Render

**Verdict: Primary candidate**

Render provides free web services that can host conventional Python applications, including FastAPI.

**Advantages**
- Supports conventional Python web applications.
- Straightforward deployment from a Git repository.
- Can expose HTTP endpoints for manual and scheduled synchronization.
- Can connect to an external PostgreSQL database.
- Suitable for a small dashboard backend.

**Limitations**
- Free services spin down after 15 minutes without inbound traffic.
- A sleeping service can take approximately one minute to become available again.
- Free services have a monthly instance-hour allowance.
- Filesystem is ephemeral.
- Free services do not include persistent disks.
- Render Cron Jobs are not free.

**Relevance to this project**

The backend can run FastAPI and use Neon PostgreSQL for persistent storage. GitHub Actions can call the synchronization endpoint daily.

The main trade-off is the cold start after inactivity. This is acceptable for a small portfolio dashboard if occasional startup delays are tolerable.

**Official documentation:**
- [Render Free Services](https://render.com/docs/free)

---

### B. Koyeb

**Verdict: Direct competitor to Render**

Koyeb offers a free web-service instance and supports conventional application deployment, including Python applications.

**Advantages**
- Supports Python applications and Docker deployments.
- Can host FastAPI.
- Provides a free web-service instance.
- Can expose HTTP endpoints for synchronization.
- Can connect to an external PostgreSQL database.
- Scales down after a longer idle period than Render's free service.

**Limitations**
- Free instance has limited compute: 0.1 vCPU and 512 MB RAM.
- Includes 2 GB SSD storage, but this should not be treated as persistent application storage.
- Free instance availability is restricted to selected regions, including Frankfurt and Washington, D.C.
- Scales to zero after one hour without traffic.
- No persistent volumes are available for the free web-service instance.
- Free PostgreSQL is limited to five hours of active time per month.

**Relevance to this project**

Koyeb is a credible alternative to Render. Its longer idle period may be useful, although both platforms have limited free compute and scale down when idle.

Use an external database such as Neon instead of relying on Koyeb's limited free PostgreSQL offering.

**Official documentation:**
- [Koyeb Pricing FAQ](https://www.koyeb.com/docs/faqs/pricing)
- [Koyeb Instance Types](https://www.koyeb.com/docs/reference/instances)

---

### C. PythonAnywhere

**Verdict: Do not prioritize**

PythonAnywhere is designed specifically for hosting Python applications. Its main disadvantages for this project are restrictions on free accounts, particularly outbound internet access and scheduled tasks.

**Advantages**
- Browser-based Python development environment.
- Supports Python web applications.
- Includes consoles for running Python commands.
- Useful for learning and experimenting with Python hosting.

**Limitations**
- One free web application.
- Two consoles.
- 512 MB storage.
- Restricted outbound internet access on free accounts.
- Limited CPU allowance for consoles and scheduled/always-on tasks.
- Newly created Beginner accounts do not receive scheduled tasks.
- External services such as Notion and Neon must be accessible under its outbound network restrictions.

**Relevance to this project**

The backend needs to communicate with both the Notion API and an external PostgreSQL database.

PythonAnywhere's outbound network restrictions create an additional compatibility requirement.

Daily synchronization would also need an external scheduler, such as GitHub Actions.

PythonAnywhere may work in some configurations, but it adds restrictions without offering a clear advantage over Render or Koyeb.

**Official documentation:**
- [PythonAnywhere Pricing](https://www.pythonanywhere.com/pricing/)
- [PythonAnywhere: Internet Access](https://help.pythonanywhere.com/pages/WhatIsTheInternet/)

---

### D. Oracle Cloud Infrastructure

**Verdict: Backup option / self-hosting alternative**

Oracle Cloud Infrastructure (OCI) offers Always Free compute resources that can run a conventional Linux server.

**Advantages**
- Can run a conventional FastAPI application.
- Offers Always Free virtual-machine resources, subject to eligibility and availability.
- Eligible Ampere A1 resources can provide up to 2 OCPUs and 12 GB RAM.
- Can run additional services such as PostgreSQL, Nginx, and background processes.
- Provides more control over the server environment than managed application platforms.
- Supports a traditional, continuously running application architecture.

**Limitations**
- Requires manual server administration.
- Responsible for operating-system updates, application deployment, firewall configuration, SSL, process management, and security.
- Always Free capacity is not guaranteed in every region.
- Resources must be provisioned in the account's home region.
- Oracle may reclaim qualifying idle Always Free compute instances under its idle-resource policy.
- Configuration and maintenance are more involved than deploying to Render or Koyeb.

**Relevance to this project**

OCI can host the entire backend and potentially the database on one virtual machine.

It offers more resources and control, but that comes with greater operational responsibility.

It is a strong option if the goal expands to include Linux administration, infrastructure management, and self-hosting.

For a small Notion dashboard, this is probably more maintenance than necessary.

**Official documentation:**
- [Oracle Cloud Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)

---

### E. Hugging Face Spaces

**Verdict: Eliminate as the primary backend host**

Hugging Face Spaces is primarily designed for publishing machine-learning demonstrations and interactive applications.

**Advantages**
- Supports Gradio applications.
- Supports Docker-based applications.
- Supports static websites.
- Convenient for showcasing machine-learning projects.
- Eligible accounts can use ZeroGPU for supported GPU-powered demonstrations.

**Limitations**
- Static Spaces cannot run a conventional Python backend.
- Ordinary CPU-backed Gradio and Docker Spaces require paid hardware for personal accounts under applicable free-tier rules.
- ZeroGPU is designed for supported GPU-powered applications, not conventional always-available FastAPI hosting.
- Its primary use case does not match a database-backed project dashboard.

**Relevance to this project**

The dashboard does not need GPU compute or a machine-learning demo environment.

It needs a conventional API that communicates with Notion and PostgreSQL.

Hugging Face Spaces is therefore not a suitable foundation for this architecture.

It could still be useful for a separate machine-learning demonstration in the future.

**Official documentation:**
- [Hugging Face Spaces Overview](https://huggingface.co/docs/hub/spaces-overview)

---

## 3. Overall Comparison

| Platform | FastAPI Hosting | Main Limitation | Verdict |
|---|---|---|---|
| Render | Yes | Free service sleeps after inactivity; ephemeral filesystem | Primary candidate |
| Koyeb | Yes | Limited free compute; scales to zero | Direct competitor |
| PythonAnywhere | Yes | Outbound network and scheduling restrictions | Do not prioritize |
| Oracle Cloud | Yes | Server administration and capacity availability | Backup |
| Hugging Face Spaces | Possible with suitable paid hardware or specialized configuration | Free hosting model mismatch | Eliminate |

---

## 4. Shortlist

### 1. Render — Primary Candidate

Best starting point for a conventional FastAPI deployment with minimal server administration.

### 2. Koyeb — Direct Competitor

Should be tested against Render before making a final hosting decision.

### 3. Oracle Cloud — Alternative

Worth considering if more control, server resources, and Linux administration experience become priorities.

PythonAnywhere and Hugging Face Spaces are not priorities for this particular project.

---

## 5. Recommended Next Step: Test Render and Koyeb

Do not finalize the hosting provider based only on published free-tier specifications.

Deploy the same small FastAPI application to both platforms and compare their actual behavior.

### Deployment Tests

1. Deploy a minimal FastAPI application.
2. Confirm that its health endpoint responds.
3. Confirm outbound HTTPS connectivity to the Notion API.
4. Confirm connectivity to the Neon PostgreSQL database.
5. Trigger a manual synchronization request.
6. Trigger synchronization through an external scheduler.
7. Leave the service idle and observe its scale-down behavior.
8. Measure the time required for the first request after inactivity.
9. Check logs, deployment failures, and resource usage.

### Evaluation Criteria

| Criterion | What to Measure |
|---|---|
| Deployment difficulty | Setup steps and configuration required |
| Startup time | Time until the application accepts requests |
| Response latency | Response time while the service is active |
| Cold-start behavior | First-request delay after inactivity |
| Notion connectivity | Whether the backend can reach the Notion API |
| PostgreSQL connectivity | Whether the backend can connect to Neon |
| Manual synchronization | Whether the API can complete a sync request |
| Scheduled synchronization | Whether an external scheduler can trigger the endpoint |
| Reliability | Errors, restarts, and deployment issues |
| Free-tier suitability | Whether the workload stays within free allowances |

---

## 6. Current Decision

**Keep Render and Koyeb as the two main candidates.**

Treat Oracle Cloud as a backup option.

Do not prioritize PythonAnywhere or Hugging Face Spaces unless project requirements change.

The next decision should be based on actual deployment tests rather than marketing specifications.

## 7. Cost Qualification

A free-tier architecture is not automatically guaranteed to remain free.

Providers can change quotas, eligibility, pricing, and account requirements.

Verify current official documentation before deployment, and monitor usage where billing is enabled.


**Notes**

-   **Render:** Suitable for a conventional FastAPI backend, but its
    filesystem is temporary and its free service sleeps.
-   **Koyeb:** Offers an actual free web service. Its free PostgreSQL
    offering is limited to five hours of active time per month, so use
    an external database instead.
-   **PythonAnywhere:** Useful for learning Python web development, but
    its free tier is restrictive for a Notion integration.
-   **Oracle Cloud:** Worth considering if you want a traditional
    virtual machine that you administer yourself. It is less
    beginner-friendly than Render.

### B. Serverless Python Hosting

Instead of running a continuously available server, these providers
execute code when requests or scheduled events arrive.

  -------------------------------------------------------------------------
  Platform|                Free possibility|        Main limitation|
  |---|---|---
 
  Google Cloud Run        2 million               Requires billing
                          requests/month plus     configuration
                          compute allowances      

  Vercel                  Hobby plan supports     Daily scheduling has
                          daily cron and          hourly precision;
                          serverless functions    personal/non-commercial
                                                  use

  AWS Lambda              1 million requests and  More complex
                          400,000                 configuration
                          GB-seconds/month        

  Azure Functions         Consumption-plan free   Requires cloud
                          grants                  subscription and
                                                  associated storage

  Netlify Functions       Free credit allowance   Credit-based usage

  Cloudflare Workers      100,000 requests/day on Python runtime is not
                          free plan               equivalent to a normal
                                                  FastAPI server
  -------------------------------------------------------------------------

  # Python Backend Hosting Assessment
**Project:** Notion Project Dashboard  
**Assessment Date:** November 7, 2026

## 1. Project Requirements

The hosting solution should support the following architecture:

- **Notion:** Source of truth for project information.
- **Python backend:** Communicates with the Notion API and synchronizes project data.
- **PostgreSQL:** Stores synchronized project data persistently.
- **React frontend:** Reads and displays data from the backend/database.
- **Manual synchronization:** A button triggers an immediate sync.
- **Automatic synchronization:** A daily scheduled sync.
- **Budget:** Preferably ₱0, without relying on a continuously running personal computer.

### Important considerations

1. Notion API credentials must remain on the backend.
2. The database must persist independently of the backend's filesystem.
3. Hosting must support Python and outbound requests to Notion.
4. Scheduled tasks must work without manually opening the website.
5. Free-tier limitations must not unexpectedly make the application unusable.

---

# 2. Traditional Python Hosting

These platforms are evaluated primarily as hosts for a conventional Python application, such as FastAPI.

## Render

**Assessment: Strong candidate**

### Advantages
- Supports conventional Python web services.
- Straightforward FastAPI deployment.
- GitHub integration simplifies deployment.
- Suitable for a backend that exposes API endpoints.
- Can connect to an external PostgreSQL database.

### Limitations
- Free web services sleep after approximately 15 minutes of inactivity.
- The service takes time to wake up after sleeping.
- Filesystem storage is ephemeral.
- Persistent disks are not included in the free web-service tier.
- Scheduled jobs are not included in the free tier.

### Assessment

Render is a practical choice for learning and deploying a conventional FastAPI backend. Its sleeping behavior is inconvenient but manageable for a personal dashboard.

Use an external PostgreSQL provider rather than storing data in local files.

**Verdict:** Recommended as the primary traditional Python hosting candidate.

---

## Koyeb

**Assessment: Strong candidate**

### Advantages
- Supports Python applications and containerized deployments.
- Offers a free web-service instance.
- Supports external database connections.
- Can deploy directly from a GitHub repository.

### Limitations
- Free instance resources are limited.
- Free instances scale to zero after inactivity.
- No persistent volumes on the free instance.
- Free PostgreSQL availability is heavily restricted.
- Free instance availability is limited to supported regions.

### Assessment

Koyeb is a reasonable alternative to Render. However, its resource limitations and scale-to-zero behavior make it important to test the actual application before committing.

**Verdict:** Recommended as a secondary traditional Python hosting candidate.

---

## PythonAnywhere

**Assessment: Low priority**

### Advantages
- Designed specifically for Python applications.
- Provides a Python-oriented development environment.
- Supports web applications and scheduled tasks on eligible plans.

### Limitations
- Free-account restrictions can affect outbound internet access.
- Free scheduled-task functionality is limited.
- Resource and application restrictions may complicate the architecture.

### Assessment

PythonAnywhere is convenient for learning Python web development, but its free-tier restrictions make it less attractive for an application that needs regular Notion API communication and database synchronization.

**Verdict:** Not recommended as the primary host.

---

## Oracle Cloud Infrastructure

**Assessment: Technically capable, but more demanding**

### Advantages
- Always Free compute resources may be sufficient for a small backend.
- Supports conventional Python applications.
- Can host PostgreSQL directly or connect to an external database.
- A virtual machine can run continuously.

### Limitations
- Requires server administration.
- Requires configuring the operating system, firewall, application server, and security.
- Free capacity depends on region and availability.
- Idle-resource reclamation policies may apply.
- More maintenance compared with managed hosting.

### Assessment

Oracle Cloud offers more control than managed platforms, but that control introduces additional responsibilities.

For a small personal dashboard, maintaining a virtual machine may be unnecessary overhead.

**Verdict:** Backup option if managed hosting becomes unsuitable.

---

## Hugging Face Spaces

**Assessment: Not recommended**

### Advantages
- Convenient for machine-learning demonstrations.
- Supports Docker-based applications.
- Useful for sharing interactive AI projects.

### Limitations
- Free Spaces are not intended to provide a conventional, continuously available FastAPI backend.
- Free hardware and sleep behavior impose limitations.
- It is primarily designed around interactive machine-learning applications.

### Assessment

Although Docker support makes it technically possible to experiment with backend applications, it is not a good fit for this dashboard.

**Verdict:** Eliminate as a primary backend host.

---

# 3. Serverless Hosting

Serverless platforms execute application code when requests or scheduled events occur instead of maintaining a conventional server process.

This can reduce hosting costs, but it changes how the backend must be deployed and operated.

## Google Cloud Run

**Assessment: Strong technical candidate**

### Advantages
- Supports conventional containerized Python applications.
- FastAPI can run without major architectural changes.
- Scales automatically.
- Offers a free usage allowance:
  - 2 million requests per month.
  - 180,000 vCPU-seconds per month under request-based pricing.
  - 360,000 GiB-seconds per month under request-based pricing.
- Cloud Scheduler provides scheduled execution, with three free jobs per billing account.

### Limitations
- Requires a Google Cloud billing account.
- Build, storage, networking, logging, and other services may introduce charges.
- Outbound data transfer costs depend on region and destination.
- More configuration than a simple managed Python host.

### Assessment

Cloud Run is one of the strongest technical options. It can run the same FastAPI application in a container.

However, its free allowance does not guarantee that the entire deployment will cost ₱0.

**Verdict:** Recommended if billing configuration and possible incidental charges are acceptable.

---

## Vercel

**Assessment: Strong candidate for a personal dashboard**

### Advantages
- Supports Python functions, including FastAPI.
- Convenient deployment from GitHub.
- Particularly suitable for React applications.
- Hobby plan includes daily cron jobs.
- No need to maintain a continuously running server.

### Limitations
- Python applications run as serverless functions rather than conventional persistent servers.
- Hobby cron jobs run once per day and may execute at any time within the scheduled hour.
- Hobby plan is restricted to personal, non-commercial use.
- Function execution duration is limited.

### Assessment

Vercel is particularly interesting because the dashboard already uses React.

A possible architecture is:

- React frontend hosted on Vercel.
- FastAPI backend deployed as Python functions.
- PostgreSQL hosted externally.
- Vercel Cron triggers the daily synchronization.

The daily cron execution window is acceptable if exact execution time is not important.

**Verdict:** One of the strongest candidates for this project.

---

## AWS Lambda

**Assessment: Technically suitable, but more complex**

### Advantages
- Free tier includes:
  - 1 million requests per month.
  - 400,000 GB-seconds of compute per month.
- Supports Python runtimes.
- Maximum execution timeout is 15 minutes.
- Can be triggered by scheduled events.
- Can expose HTTP endpoints through Lambda Function URLs.

### Limitations
- FastAPI requires an adapter such as Mangum.
- Uses a function-based execution model.
- Requires additional AWS configuration.
- IAM, event scheduling, logging, and deployment introduce complexity.
- Other AWS services may incur separate charges.

### Assessment

AWS Lambda can support the backend, but it requires learning a different deployment model.

It is a reasonable option for someone specifically interested in AWS, but not the simplest route for this project.

**Verdict:** Technically viable, but lower priority.

---

## Azure Functions

**Assessment: Low priority**

### Advantages
- Supports Python.
- Supports scheduled execution through timer triggers.
- Offers serverless execution.
- Provides free usage grants on eligible plans.

### Limitations
- The newer Flex Consumption plan has different free allowances from the legacy Consumption plan.
- Flex Consumption grants include 250,000 executions and 100,000 GB-seconds.
- Storage and networking may introduce additional charges.
- Requires Azure-specific configuration and deployment knowledge.

### Assessment

Azure Functions can handle the workload, but its hosting models and associated storage requirements introduce unnecessary complexity.

**Verdict:** Not recommended as a first choice.

---

## Netlify Functions

**Assessment: Not suitable for the Python backend**

### Advantages
- Convenient React frontend hosting.
- Git-based deployment.
- Free plan available.
- Supports serverless functions.

### Limitations
- Native Functions support does not provide a conventional Python runtime.
- Its primary function runtimes are JavaScript/TypeScript and Go.
- Free usage is governed by a credit system.
- Projects can be paused after exhausting their monthly credits.

### Assessment

Netlify is a possible frontend host, but it does not fit the requirement for a Python backend.

**Verdict:** Eliminate as a Python backend host.

---

## Cloudflare Workers

**Assessment: Interesting alternative; requires testing**

### Advantages
- Officially supports Python Workers.
- FastAPI can run through an ASGI adapter.
- Free plan includes:
  - 100,000 requests per day.
  - Five Cron Triggers per account.
  - 128 MB memory per Worker.
- Can execute scheduled tasks.
- Does not require a conventional server to remain running.

### Limitations
- Python runs through Pyodide, which uses WebAssembly.
- It is not identical to running Python on a conventional CPython server.
- Some Python packages, particularly those requiring native extensions, may not work.
- Free HTTP requests have a 10 ms CPU-time limit.
- Multi-page Notion synchronization may require more CPU time than expected.
- PostgreSQL driver compatibility must be tested.

### Assessment

Cloudflare Workers is more capable than initially expected. It officially supports FastAPI, making it a genuine candidate.

However, the execution environment differs from conventional Python hosting. The Notion synchronization process and PostgreSQL connection must be tested before relying on it.

**Verdict:** Keep as an experimental candidate, not the first deployment choice.

---

# 4. Overall Comparison

| Platform | Python Support | Free-Tier Suitability | Main Concern | Verdict |
|---|---|---|---|---|
| Render | Conventional Python | Good | Sleeps when idle | Recommended |
| Koyeb | Conventional Python | Good | Resource limits and scale-to-zero | Recommended |
| Vercel | Python Functions | Good | Serverless execution model | Recommended |
| Google Cloud Run | Conventional Python containers | Good | Billing and possible additional charges | Recommended |
| Cloudflare Workers | Python via Pyodide | Conditional | CPU limit and package compatibility | Experimental |
| AWS Lambda | Python runtime | Good | Additional AWS configuration | Alternative |
| Oracle Cloud | Conventional Python | Potentially good | Server administration | Backup |
| Azure Functions | Python runtime | Conditional | Hosting and storage complexity | Low priority |
| PythonAnywhere | Conventional Python | Limited | Free-tier restrictions | Low priority |
| Netlify Functions | No native Python runtime | Unsuitable | No conventional Python runtime | Eliminate |
| Hugging Face Spaces | Docker/Python | Limited | Not designed for this workload | Eliminate |

---

# 5. Overall Ranking

Considering the project requirements, ease of deployment, Python compatibility, and free-tier suitability:

| Rank | Platform | Reason |
|---:|---|---|
| 1 | Render | Straightforward conventional FastAPI hosting |
| 2 | Koyeb | Strong alternative to Render |
| 3 | Vercel | Convenient React and Python Functions deployment |
| 4 | Google Cloud Run | Excellent container support, but billing complexity |
| 5 | Cloudflare Workers | Promising, but requires compatibility and CPU testing |
| 6 | AWS Lambda | Capable, but introduces additional infrastructure concepts |
| 7 | Oracle Cloud | Powerful, but requires server maintenance |
| 8 | Azure Functions | Capable, but unnecessary complexity |
| 9 | PythonAnywhere | Free-tier restrictions |
| 10 | Netlify Functions | No native Python runtime |
| 11 | Hugging Face Spaces | Poor fit for a conventional backend |

This ranking prioritizes simplicity and suitability for the intended dashboard. It is not a ranking of raw performance.

---

# 6. Recommended Architecture

The following architecture keeps Notion as the source of truth while allowing the website to read from PostgreSQL.

```text
                    NOTION
                (Source of Truth)
                       |
                       |
                 Notion API
                       |
                       v
              PYTHON BACKEND
                  FastAPI
                       |
              +--------+--------+
              |                 |
              v                 v
        Manual Sync        Daily Sync
         (API Route)       (Scheduler)
              |                 |
              +--------+--------+
                       |
                       v
                 PostgreSQL
                (Persistent DB)
                       |
                       |
                       v
                REACT FRONTEND
                 (Dashboard)

#### Google Cloud Run

A strong Python candidate.

-   Supports containerized FastAPI applications.
-   Can scale to zero.
-   Has a monthly free compute allowance.
-   Can use Google Cloud Scheduler for daily synchronization.
-   Cloud Scheduler provides three jobs free per billing account, enough
    for one daily sync.

**Caveat:** Google Cloud requires billing configuration. Staying within
free quotas is possible, but this is not a hard guarantee that the bill
can never be nonzero.

#### AWS Lambda

-   Supports Python.
-   Executes on demand.
-   Can be triggered by API Gateway and scheduled events.
-   Has a generous request-based free allowance.

It is powerful, but AWS has more concepts to learn than Render.

#### Cloudflare Workers

-   Excellent free request allowance.
-   Built-in Cron Triggers.
-   Can connect to Cloudflare D1.
-   Supports Python through its Python Workers runtime.

However, its Python runtime uses a different execution model and has
strict CPU limits. It is not the best choice if your primary learning
goal is conventional FastAPI development.

#### Vercel

-   Supports Python functions.
-   Supports daily scheduled execution on Hobby.
-   Convenient for hosting a frontend and API together.

The Hobby plan is limited to personal, non-commercial usage, and
scheduled jobs can run within an approximately one-hour window.

### C. Platforms That Are Not Genuinely Free for Ongoing Backend Hosting

These are worth knowing, but they are not good foundations for a ₱0
architecture.

  -----------------------------------------------------------------------
  Platform                            Situation
  ----------------------------------- -----------------------------------
  Railway                             Offers limited trial credits, not a
                                      permanent unrestricted free server

  Fly.io                              Pay-as-you-go; do not assume an
                                      ongoing free allowance

  Heroku                              No permanent free dynos

  Replit                              Free development environment, but
                                      do not assume free persistent
                                      deployment

  Glitch                              Hosting service discontinued
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 2. Frontend Hosting Platforms

These host your website: React, HTML, CSS, JavaScript, and static
assets. Most do not execute a conventional Python backend.

  Platform              Free possibility         Best use
  --------------------- ------------------------ ------------------------
  GitHub Pages          Free                     Static portfolio
  Cloudflare Pages      Free                     Static websites
  Vercel                Hobby plan               React and Next.js
  Netlify               Free credit-based plan   React and static sites
  Render Static Sites   Free                     Static websites
  Firebase Hosting      Free quota               Static websites
  Surge                 Free basic publishing    Simple static sites

**Useful details**

-   Cloudflare Pages allows 500 builds per month on its free plan.
-   GitHub Pages is convenient if your source code is already on GitHub.
-   Netlify has moved to a credit-based model. Production deployments
    and bandwidth consume credits.
-   Vercel is particularly convenient for React and Next.js
    applications.

**Shortlist for this dashboard:** Cloudflare Pages, Vercel, and GitHub
Pages.


# Frontend Hosting Platform Assessment

**Project:** Notion Project Dashboard  
**Assessment Date:** November 7, 2026

---

# 1. Project Requirements

The frontend hosting provider will serve the dashboard's React application and its static assets.

The frontend consists of:

- React components
- JavaScript
- HTML
- CSS
- Images and icons
- Other static assets

The frontend will retrieve project information from the Python backend rather than directly accessing Notion or PostgreSQL.

## Intended architecture

```text
                    USER
                     |
                     v
              FRONTEND HOST
               React App
                     |
                     | HTTPS Request
                     v
              PYTHON BACKEND
                  FastAPI
                     |
                     v
               NEON POSTGRES
                     |
                     v
              PROJECT DATA
```

The hosting provider should ideally:

1. Support React and modern JavaScript build tools.
2. Integrate with GitHub for automatic deployments.
3. Provide HTTPS.
4. Support custom domains.
5. Offer sufficient bandwidth for a small dashboard.
6. Support client-side routing.
7. Allow environment-specific frontend configuration.
8. Cost ₱0.

## Important security consideration

The frontend is publicly downloadable, even if the dashboard itself is intended for personal use.

Never place these credentials in React code:

- Notion API token
- PostgreSQL connection string
- Database password
- Backend synchronization secret

Environment variables embedded during a frontend build can become visible in the generated JavaScript.

The frontend should only contain public configuration, such as the backend API URL.

Authentication and authorization must be enforced by the backend if project information is private.

---

# 2. Frontend Hosting Platforms

## 2.1 GitHub Pages

**Assessment: Good for simple static websites**

### Free allowance

| Resource | Free allowance or limit |
|---|---|
| Hosting | Free |
| Published site size | Maximum 1 GB |
| Recommended source repository size | 1 GB |
| Bandwidth | 100 GB/month soft limit |
| Builds | 10 builds/hour soft limit |
| HTTPS | Supported |
| Custom domains | Supported |

### Advantages

- Free static website hosting.
- Convenient if the source code is already on GitHub.
- Supports React after building the application into static files.
- Supports custom domains.
- Supports HTTPS.
- Can automatically deploy through GitHub Actions.
- No conventional server needs to remain running.

### Limitations

- Static hosting only.
- Cannot execute a conventional Python backend.
- No server-side environment variables for protecting secrets.
- Published site size is limited to 1 GB.
- Bandwidth has a soft limit of 100 GB/month.
- Not designed to host commercial SaaS applications.
- React applications using client-side routing may need additional configuration.

### Assessment

GitHub Pages is convenient for portfolios, documentation, and simple static websites.

It can also host a React dashboard that retrieves information from an external FastAPI backend.

However, it is less convenient for applications that need more sophisticated routing or deployment configuration.

A React application can be built using Vite and deployed through GitHub Actions.

One important consideration is that GitHub Pages does not provide a conventional server-side fallback for every client-side route. A React application using BrowserRouter may require additional routing configuration or HashRouter.

**Verdict:** Viable, but not the strongest option for this dashboard.

### Sources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Pages Limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [GitHub Pages Usage Restrictions](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)

---

## 2.2 Cloudflare Pages

**Assessment: Strongest overall candidate**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Hosting | Free |
| Builds | 500/month |
| Concurrent builds | 1 |
| Build timeout | 20 minutes |
| Files per site | 20,000 |
| Maximum individual file size | 25 MiB |
| Static asset requests | Unlimited and free |
| Custom domains | Up to 100 per project |

### Advantages

- Free static website hosting.
- Excellent support for React and Vite applications.
- Global content delivery network.
- Static asset requests are free and unlimited.
- Supports custom domains.
- Provides HTTPS automatically.
- Supports GitHub integration.
- Supports preview deployments.
- Supports rollbacks.
- Can connect to external APIs.
- Does not require a continuously running server.

### Limitations

- Static assets are subject to file count and file size limits.
- Free builds are limited to 500 per month.
- Only one build can run at a time on the free plan.
- Pages Functions introduce separate Workers usage limits.
- More advanced server-side functionality requires additional Cloudflare configuration.

### Assessment

Cloudflare Pages is particularly suitable for a React dashboard.

The project can be built into static files and distributed through Cloudflare's global network.

The 500-build monthly allowance is more than enough for normal development.

The unlimited free static asset requests are especially attractive because the dashboard may be opened repeatedly throughout the day.

Cloudflare also allows the frontend to communicate with an external FastAPI backend. The backend does not need to be hosted on Cloudflare.

An important distinction:

- Static asset requests are free and unlimited.
- Pages Functions requests are subject to Cloudflare Workers limits.

The dashboard can avoid needing Pages Functions if all dynamic operations are handled by the external FastAPI backend.

Cloudflare's current documentation also encourages developers to consider Workers for new full-stack applications. However, Pages remains a practical option for a purely static React frontend.

**Verdict:** Best overall frontend hosting candidate.

### Sources

- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Cloudflare Pages Limits](https://developers.cloudflare.com/pages/platform/limits/)
- [Cloudflare Pages Functions Pricing](https://developers.cloudflare.com/pages/functions/pricing/)

---

## 2.3 Vercel

**Assessment: Strong candidate, especially for React and Next.js**

### Free allowance

| Resource | Hobby plan |
|---|---|
| Hosting | Free |
| Projects | Up to 200 |
| Concurrent builds | 1 |
| Build duration | Up to 45 minutes |
| Static deployment | Supported |
| HTTPS | Supported |
| Custom domains | Supported |
| Function invocations | 1 million included |
| Usage restrictions | Personal, non-commercial use |

### Advantages

- Excellent React and Next.js support.
- GitHub integration.
- Automatic deployments.
- Preview deployments for branches and pull requests.
- Global content delivery network.
- HTTPS and custom domains.
- Convenient environment variable management.
- Supports static frontend hosting.
- Can also host supported serverless functions.

### Limitations

- Hobby plan is restricted to personal, non-commercial use.
- Usage limits apply to functions and other platform features.
- Exceeding certain free allowances may require waiting for the usage period to reset.
- More advanced features may require a paid plan.
- Serverless functionality is different from a conventional persistent backend.

### Assessment

Vercel is one of the most convenient platforms for deploying React applications.

Its GitHub integration makes the development workflow straightforward:

```text
GitHub Repository
       |
       v
   Vercel Build
       |
       v
  React Production Build
       |
       v
   Global CDN
       |
       v
      Users
```

It is especially attractive if the project uses Next.js.

For a conventional React + Vite application, however, Cloudflare Pages can provide a simpler static hosting arrangement.

Vercel's Hobby plan is suitable only if the project qualifies as personal, non-commercial use.

**Verdict:** Recommended alternative. Particularly attractive if the project uses Next.js or already deploys other components on Vercel.

### Sources

- [Vercel Hobby Plan](https://vercel.com/docs/plans/hobby)
- [Vercel Pricing](https://vercel.com/pricing)
- [Vercel Limits](https://vercel.com/docs/limits)

---

## 2.4 Netlify

**Assessment: Good platform, but its credit system needs consideration**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Hosting | Free |
| Monthly credits | 300 |
| Production deployment | 15 credits |
| Bandwidth | 20 credits/GB |
| Web requests | 2 credits/10,000 requests |
| Compute | 10 credits/GB-hour |
| Custom domains | Supported |
| HTTPS | Supported |

### Advantages

- Supports React and other frontend frameworks.
- GitHub integration.
- Automatic deployments.
- Deploy previews.
- Custom domains.
- HTTPS.
- Global content delivery network.
- Supports serverless functions.
- Useful for static websites.

### Limitations

- Uses a credit-based free plan.
- Production deployments consume 15 credits each.
- Bandwidth consumes 20 credits per GB.
- Web requests consume credits.
- Functions and other compute features consume additional credits.
- The free plan has a hard monthly credit limit.
- Projects can be affected when the monthly allowance is exhausted.

### Assessment

Netlify remains a capable frontend hosting platform.

However, its credit-based pricing makes it less predictable than Cloudflare Pages for a dashboard that will be accessed regularly.

For example, production deployments alone consume:

```text
300 monthly credits / 15 credits per deployment
= 20 production deployments
```

This is before accounting for bandwidth, requests, or compute.

For a small dashboard, the free allowance may still be sufficient. However, Cloudflare Pages has a simpler static asset pricing model.

**Verdict:** Viable alternative, but lower priority than Cloudflare Pages and Vercel.

### Sources

- [Netlify Pricing](https://www.netlify.com/pricing/)
- [Netlify Credit System](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)

---

## 2.5 Render Static Sites

**Assessment: Good alternative for a simple frontend**

### Free allowance

| Resource | Free allowance |
|---|---|
| Hosting | Free |
| Static websites | Supported |
| Custom domains | Supported |
| HTTPS | Supported |
| GitHub integration | Supported |
| Bandwidth | Counts against workspace included usage |
| Build pipeline | Counts against workspace included usage |

### Advantages

- Free static website hosting.
- Supports React and other frontend frameworks.
- Automatic deployments from GitHub.
- Custom domains.
- Managed TLS certificates.
- Preview deployments.
- Global content delivery network.
- Does not sleep like a free Render web service.

### Limitations

- Static sites consume workspace bandwidth allowances.
- Builds consume pipeline minutes.
- Additional usage may introduce charges.
- Does not execute a conventional Python backend as part of a static site.
- Requires a separate Render Web Service if the backend is also hosted on Render.

### Assessment

Render Static Sites are convenient if the Python backend is already hosted on Render.

The frontend and backend can be deployed under the same provider while remaining separate services.

For example:

```text
Render Static Site
       |
       v
 React Dashboard
       |
       v
Render Web Service
       |
       v
    FastAPI
       |
       v
 Neon PostgreSQL
```

This is a simple architecture, but the free-tier bandwidth and build pipeline usage should be monitored.

The static site itself does not sleep when inactive.

**Verdict:** Good alternative, especially if the backend is hosted on Render.

### Sources

- [Render Static Sites](https://render.com/docs/static-sites)
- [Render Free Services](https://render.com/docs/free)
- [Render Pricing](https://render.com/pricing)

---

## 2.6 Firebase Hosting

**Assessment: Good static hosting option**

### Free allowance

| Resource | Spark plan |
|---|---:|
| Hosting storage | 10 GB |
| Data transfer | 10 GB/month |
| Custom domains | Supported |
| HTTPS | Supported |
| Global CDN | Included |
| Individual file size | Maximum 2 GB |

### Advantages

- Supports React and other static frontend frameworks.
- Free Spark plan.
- No payment method required for the Spark plan.
- Custom domains.
- Automatic HTTPS.
- Global content delivery network.
- Supports multiple hosting sites within a project.
- Can integrate with Firebase Authentication if needed.

### Limitations

- Data transfer is limited to 10 GB/month.
- Hosting storage is limited to 10 GB.
- If the Spark plan exceeds its free transfer quota, sites can be disabled until the next monthly period.
- More advanced Firebase and Google Cloud functionality may require the Blaze plan.
- Does not provide a conventional Python backend.

### Assessment

Firebase Hosting is a practical static hosting option.

Its 10 GB storage allowance is generous for a React dashboard.

The main limitation is the 10 GB monthly data transfer allowance.

For a small dashboard with relatively few users, this may be sufficient.

However, Cloudflare Pages offers a more attractive static asset request and bandwidth arrangement.

**Verdict:** Good alternative, but not the first choice.

### Sources

- [Firebase Pricing](https://firebase.google.com/pricing)
- [Firebase Hosting Usage and Quotas](https://firebase.google.com/docs/hosting/usage-quotas-pricing)
- [Firebase Pricing Plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans)

---

## 2.7 Surge

**Assessment: Good for simple static publishing, but limited platform features**

### Free allowance

| Resource | Free allowance |
|---|---|
| Hosting | Free |
| Projects | Unlimited |
| Domains | Unlimited |
| Custom domains | Supported |
| SSL certificates | Included |
| Publishing | 500/day per account |
| Project size | 450 MB |
| Files per project | 10,100 |
| Bandwidth billing | No bandwidth billing |

### Advantages

- Free static hosting.
- Unlimited projects.
- Custom domains.
- Automatic SSL certificate provisioning.
- Simple command-line deployment.
- Supports continuous deployment through external CI/CD tools.
- No bandwidth billing.
- Supports clean URLs and basic static hosting features.

### Limitations

- Primarily command-line oriented.
- Less integrated GitHub deployment workflow than Vercel or Cloudflare Pages.
- Free plan does not include some server-side features.
- Password protection and server-side routing features require the paid plan.
- Less convenient for larger frontend development workflows.

### Assessment

Surge is useful for quickly publishing a static website.

However, it is more focused on simple deployment than a complete frontend development workflow.

For a React dashboard, it can host the generated build output, but Cloudflare Pages and Vercel offer more convenient GitHub integration and deployment previews.

**Verdict:** Low priority. Suitable for simple prototypes, but not recommended as the primary dashboard host.

### Sources

- [Surge Pricing](https://surge.sh/pricing)
- [Surge Plans](https://surge.sh/help/upgrading-to-surge-plus)
- [Surge SSL Documentation](https://surge.sh/docs/platform/ssl)

---

# 3. Overall Comparison

| Platform | React Support | Free Hosting | Main Limitation | Verdict |
|---|---|---|---|---|
| Cloudflare Pages | Yes | Free | Build and asset limits | Recommended |
| Vercel | Yes | Hobby | Personal, non-commercial restriction | Recommended |
| GitHub Pages | Yes, after build | Free | Static-only and usage restrictions | Viable |
| Render Static Sites | Yes | Free | Workspace bandwidth and build limits | Viable |
| Firebase Hosting | Yes | Spark | 10 GB/month transfer | Alternative |
| Netlify | Yes | 300 credits/month | Credit-based usage | Alternative |
| Surge | Yes, after build | Free | Limited deployment workflow | Low priority |

---

# 4. Comparison of the Strongest Candidates

The three strongest candidates are Cloudflare Pages, Vercel, and GitHub Pages.

| Category | Cloudflare Pages | Vercel | GitHub Pages |
|---|---|---|---|
| React support | Yes | Yes | Yes, after build |
| Vite support | Yes | Yes | Yes, through build workflow |
| GitHub integration | Yes | Yes | Native |
| Free static hosting | Yes | Yes | Yes |
| Build allowance | 500/month | Plan limits apply | 10/hour soft limit |
| Static bandwidth | Unlimited free static asset requests | Subject to plan usage policies | 100 GB/month soft limit |
| Custom domains | Yes | Yes | Yes |
| HTTPS | Yes | Yes | Yes |
| Preview deployments | Yes | Yes | Requires additional workflow |
| Client-side routing | Supported | Supported | Requires additional configuration |
| Best use | Static frontend | React/Next.js applications | Simple static websites |

## Cloudflare Pages advantages

- Unlimited free static asset requests.
- Generous monthly build allowance.
- Global content delivery.
- Suitable for React + Vite.
- Good separation between frontend and backend.

## Vercel advantages

- Excellent developer experience.
- Strong React and Next.js support.
- Convenient deployment previews.
- Integrated serverless functionality.
- Good if the backend is also deployed on Vercel.

## GitHub Pages advantages

- Simple integration with GitHub.
- No additional frontend hosting account is necessary.
- Suitable for static portfolios and documentation.
- Easy to use with GitHub Actions.

## Decision

Cloudflare Pages is the strongest overall candidate for the current dashboard.

Vercel is the closest alternative.

GitHub Pages remains viable, but its limitations make it less attractive for an application rather than a simple portfolio.

---

# 5. Recommended Frontend Architecture

The frontend should remain independent of the backend hosting provider.

For example:

```text
                  USER
                    |
                    v
             CLOUDFLARE PAGES
                 React
                    |
                    |
              HTTPS Request
                    |
                    v
              FASTAPI BACKEND
               Render/Koyeb
                    |
                    v
              NEON POSTGRES
                    |
                    v
              PROJECT DATA
```
Frontend Framework Comparison and Complete Technology Stack Assessment
Objective: Choose technologies for the Notion Project Dashboard, with PostgreSQL as the source of truth, two-way Notion synchronization, editable project/task records, and a target hosting cost of ₱0.

The important distinction is that we're evaluating two different things:
1. Frontend frameworks: Technologies used to build the dashboard interface.
2. Hosting and infrastructure: Services that run, store, and synchronize the application.
I'll compare the mainstream frontend options rather than literally every JavaScript framework ever published. I'll also distinguish UI frameworks from full-stack frameworks, because they solve different problems.
1. Frontend frameworks
First, the main candidates
Technology	Type	Main characteristic
React	UI library	Large ecosystem, reusable components
Vue	UI framework	HTML-oriented templates and approachable reactivity
Angular	Full frontend framework	Comprehensive, opinionated application structure
Svelte	UI framework/compiler	Compiles components into JavaScript
SolidJS	UI framework	Fine-grained reactivity
Preact	UI library	Lightweight React-compatible alternative
Qwik	UI framework	Resumability and fast initial interactivity
Lit	Web component library	Standards-based reusable custom elements
Astro	Web framework	Content-focused sites and component islands
Ember	Full frontend framework	Convention-driven application development
Alpine.js	Lightweight framework	Small interactive behaviors in HTML
HTMX	HTML interaction library	Server-driven interactions using HTML attributes

These aren't all direct substitutes. For example, Astro is optimized for content-driven sites, whereas React and Vue are commonly used to build application interfaces. 
Docs+3

Direct comparison
Assessment based on this dashboard's needs, not a universal framework ranking.
Framework	Advantages	Disadvantages	Fit
React	Huge ecosystem, extensive component libraries, mature tooling	More choices to make; JSX and state management take learning	Excellent
Vue	Approachable templates, good documentation, built-in reactivity	Smaller ecosystem than React	Excellent
Svelte	Concise syntax, compiler optimizations, less boilerplate	Smaller ecosystem and fewer established dashboard integrations	Excellent
Angular	Routing, dependency injection, forms, and application structure included	More concepts and conventions to learn	Good
Preact	Lightweight and React-compatible	Some React libraries and integrations need compatibility checks	Good
SolidJS	Fine-grained reactivity, efficient updates	Smaller ecosystem and fewer ready-made dashboard solutions	Good
Qwik	Resumability and optimized initial loading	More specialized concepts; performance advantages are less important for this use case	Moderate
Ember	Strong conventions and comprehensive application structure	Less commonly chosen for new small projects	Moderate
Lit	Native web components, framework-independent components	Not as convenient as a complete application framework	Moderate
Astro	Excellent for content-heavy sites and static pages	Its primary architecture is less suited to a highly interactive dashboard	Low
HTMX	HTML-driven requests, can work directly with FastAPI-rendered HTML	Different development approach; less convenient for complex client-side interfaces	Alternative architecture
Alpine.js	Lightweight, easy to add small interactions to HTML	Not ideal for a large, component-heavy application	Low

Sources: official documentation for React, Vue, Svelte, Angular, Solid, Preact, Qwik, Lit, Astro and HTMX.
What the comparison means
React: Best overall ecosystem. There are established solutions for tables, charts, forms, authentication, date pickers, and component libraries. This matters because your dashboard will have many interactive elements.

Vue: Probably the most approachable alternative. Its single-file components let you keep template, logic, and styles together. The official Vue documentation recommends Composition API and Single-File Components for full applications. 
Vue.js+1


Svelte: Particularly appealing if you want less boilerplate. Svelte uses a compiler to transform components into JavaScript, while SvelteKit provides routing and application features. 
Svelte Docs+1


Angular: A good choice for larger teams and applications with strict architectural conventions. It already includes many features that other frameworks require additional libraries to provide. 
Angular


SolidJS: Technically interesting. Its fine-grained reactivity updates targeted parts of the interface rather than relying on React-style component re-execution. Its smaller ecosystem is the main drawback for this project. 
SolidJS Documentation+1

2. Popularity and developer satisfaction
The State of JavaScript 2025 survey is useful for understanding the ecosystem, although its results represent survey respondents rather than all developers.

Some notable findings:
- React remains the dominant frontend option in usage.
- Vue and Svelte have strong satisfaction and retention.
- Solid has particularly high satisfaction among its smaller user base.
- The framework ecosystem has remained relatively stable rather than constantly replacing its leading technologies. 
  2025.stateofjs.com+1
The takeaway: choosing React isn't simply following a trend. Its ecosystem and availability of learning resources are practical advantages.
3. Meta-frameworks: Next.js, Nuxt, SvelteKit, and others
These deserve a separate comparison because they're built around existing frontend frameworks.
Technology	Based on	What it adds
Next.js	React	Routing, server rendering, server-side functionality
Nuxt	Vue	Routing, SSR, data fetching, full-stack features
SvelteKit	Svelte	Routing, SSR, data loading, deployment support
SolidStart	SolidJS	Routing and full-stack application features
Qwik City	Qwik	Routing, data loading, endpoints
Astro	Multiple UI frameworks	Static-first pages and interactive component islands

Official references: 
Next.js+4


Do we need one?

Probably not.

Your existing FastAPI backend already handles:
- Server-side business logic.
- Database access.
- Authentication, if needed.
- Notion API integration.
- Synchronization.
Adding Next.js or Nuxt would introduce another application layer without solving a requirement that FastAPI cannot already handle.

For this project, a client-side application is sufficient.
4. Vite: What is it, and why does it matter?









Vite

Build tool, not a frontend framework.
Official documentation

Vite provides:
- A local development server.
- Fast hot module replacement.
- Production builds.
- Optimized static frontend files.
It supports React, Vue, Svelte, Preact, Lit, Solid, Qwik, and vanilla JavaScript. 
Vite+1


For example:
React + Vite
Vue + Vite
Svelte + Vite
SolidJS + Vite


All of these can produce static files that Cloudflare Pages can host. 
Vite+1


5. Frontend framework ranking for your project
My recommendation: React + Vite
Rank	Technology	Reason
1	React + Vite	Best overall ecosystem, dashboard libraries, and flexibility
2	Vue + Vite	Easier learning curve and excellent application capabilities
3	Svelte + Vite	Concise code and good application performance
4	Angular	Strong structure, but more complexity than necessary
5	Preact + Vite	Lightweight, but ecosystem compatibility needs checking
6	SolidJS + Vite	Strong reactivity, smaller ecosystem
7	Qwik	Specialized performance architecture
8	Ember	Comprehensive, but less suitable for a small new project
9	Lit	Better for reusable web components than a complete dashboard
10	Astro	Better suited to content-focused websites
11	HTMX	Better suited to a server-rendered architecture
12	Alpine.js	Better for small interactive enhancements

### Suggested deployment configuration

For a React + Vite project:

| Setting | Value |
|---|---|
| Framework preset | React / Vite |
| Root directory | `frontend` (if using a monorepo) |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node.js version | Compatible with the project's dependencies |

The frontend should use an environment variable for the backend URL.

Example:

```env
VITE_API_URL=https://your-backend.example.com
```

The frontend can then access the API through:

```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

The API URL is public configuration, not a secret.

### CORS configuration

Since the frontend and backend may use different domains, the FastAPI backend must allow requests from the deployed frontend origin.

For example:

```text
Frontend:
https://dashboard.pages.dev

Backend:
https://api.example.com
```

The backend should configure CORS to allow the intended frontend origin.

Avoid allowing every origin if the application handles private project information.

### Client-side routing

If the dashboard uses React Router, verify that direct navigation to nested routes works.

For example:

```text
/dashboard
/projects
/projects/123
/settings
```

Refreshing a nested route should not produce a 404 error.

Cloudflare Pages and Vercel support SPA deployment patterns. GitHub Pages may require additional routing configuration.

---

# 6. Security Considerations

The frontend host does not automatically make the dashboard private.

Even if the repository is private, the deployed website may be publicly accessible.

Important rules:

1. Never put the Notion API token in React.
2. Never put PostgreSQL credentials in React.
3. Never put the synchronization secret in React.
4. Authenticate requests that access private project information.
5. Enforce authorization in FastAPI.
6. Configure CORS for the intended frontend domain.
7. Avoid treating an obscure frontend URL as authentication.
8. Do not rely on hidden buttons or frontend checks to protect backend endpoints.

If the dashboard will contain private information, implement authentication before exposing the project data through the public API.

---

# 7. Final Recommendation

**Primary choice: Cloudflare Pages**

Recommended ranking:

1. **Cloudflare Pages:** Best overall fit for a static React frontend.
2. **Vercel:** Best alternative, especially for Next.js.
3. **Render Static Sites:** Convenient if the backend is also hosted on Render.
4. **Firebase Hosting:** Good alternative with a generous storage allowance.
5. **GitHub Pages:** Suitable for simple static projects, but less flexible.
6. **Netlify:** Capable, but its credit system makes usage less predictable.
7. **Surge:** Useful for simple prototypes, but less suitable for the complete dashboard workflow.

## Suggested complete hosting stack

| Component | Recommended Platform |
|---|---|
| Frontend | Cloudflare Pages |
| Python backend | Render or Koyeb |
| Database | Neon PostgreSQL |
| Source of truth | Notion |
| Daily scheduler | GitHub Actions |
| Manual synchronization | React calling FastAPI |

This architecture keeps the frontend, backend, database, and scheduler independent.

If one provider becomes unsuitable, the other components can remain in place.

---

# 8. Suggested Next Steps

Before committing to Cloudflare Pages:

1. Build the React application locally.
2. Confirm that `npm run build` succeeds.
3. Push the frontend to GitHub.
4. Connect the repository to Cloudflare Pages.
5. Configure the build output directory.
6. Set the backend API URL as a frontend environment variable.
7. Deploy the static site.
8. Test API requests to FastAPI.
9. Configure CORS on the backend.
10. Test direct navigation and page refreshes.
11. Verify that no secrets are included in the generated JavaScript.
12. Test the dashboard from another browser or device.

**Do not choose a frontend provider based only on framework support.** All the major candidates can host a React application. The more important differences are deployment workflow, usage limits, routing, and how well the platform fits the rest of the architecture.

---

# 9. Sources

## GitHub Pages
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Pages Limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)

## Cloudflare Pages
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Cloudflare Pages Limits](https://developers.cloudflare.com/pages/platform/limits/)
- [Cloudflare Pages Functions Pricing](https://developers.cloudflare.com/pages/functions/pricing/)

## Vercel
- [Vercel Hobby Plan](https://vercel.com/docs/plans/hobby)
- [Vercel Pricing](https://vercel.com/pricing)
- [Vercel Limits](https://vercel.com/docs/limits)

## Netlify
- [Netlify Pricing](https://www.netlify.com/pricing/)
- [Netlify Credit System](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)

## Render
- [Render Static Sites](https://render.com/docs/static-sites)
- [Render Free Services](https://render.com/docs/free)
- [Render Pricing](https://render.com/pricing)

## Firebase Hosting
- [Firebase Pricing](https://firebase.google.com/pricing)
- [Firebase Hosting Usage and Quotas](https://firebase.google.com/docs/hosting/usage-quotas-pricing)
- [Firebase Pricing Plans](https://firebase.google.com/docs/projects/billing/firebase-pricing-plans)

## Surge
- [Surge Pricing](https://surge.sh/pricing)
- [Surge Plans](https://surge.sh/help/upgrading-to-surge-plus)
- [Surge SSL Documentation](https://surge.sh/docs/platform/ssl)

---

**Assessment note:** Free-tier quotas, usage policies, and pricing can change. Verify the current provider documentation before deployment.


------------------------------------------------------------------------

## 3. Database and Storage Platforms

The Python backend will synchronize Notion data into a persistent
database. The website will retrieve data from this database rather than
querying Notion on every visit.

### A. SQL / Relational Databases

These are the preferred options for this project.

  -----------------------------------------------------------------------
  Platform                Free allowance          Important limitation
  ----------------------- ----------------------- -----------------------
  Supabase                500 MB PostgreSQL; 5 GB Pauses after a week of
                          egress                  inactivity

  Neon                    1 GB per project; 100   Compute scales to zero
                          CU-hours/month          

  Turso                   5 GB storage; 500M rows SQLite/libSQL rather
                          read/month; 10M rows    than PostgreSQL
                          written/month           

  Cloudflare D1           5 GB total storage; 5M  Designed for Cloudflare
                          rows read/day; 100K     Workers
                          written/day             

  Firebase Firestore      1 GiB; 50K reads/day;   NoSQL rather than
                          20K writes/day          relational SQL

  Render PostgreSQL       1 GB                    Free database expires
                                                  after 30 days
  -----------------------------------------------------------------------


# Database and Storage Platform Assessment

**Project:** Notion Project Dashboard  
**Assessment Date:** November 7, 2026

---

# 1. Project Requirements

The database will store a synchronized copy of the information in Notion.

The intended architecture is:

```text
              NOTION
          (Source of Truth)
                 |
                 v
          PYTHON BACKEND
              FastAPI
                 |
                 v
           PostgreSQL
        (Persistent Storage)
                 |
                 v
          REACT FRONTEND
             Dashboard
```

The database should:

- Persist data independently of the Python backend.
- Support structured project records.
- Support relationships between projects, tasks, categories, and other entities.
- Allow the backend to insert, update, and retrieve records.
- Support concurrent reads from the website.
- Remain accessible when the backend restarts or sleeps.
- Ideally cost ₱0.

## Preferred database type: PostgreSQL

PostgreSQL is the preferred choice because the project has structured information and potentially related entities.

For example:

- Projects have multiple tasks.
- Projects have categories or statuses.
- Tasks belong to projects.
- Projects have creation and modification timestamps.
- Synchronization records track when data was last updated.

These relationships fit a relational database naturally.

SQLite-based alternatives are still viable, but PostgreSQL provides a more conventional setup for learning backend development and working with FastAPI.

---

# 2. SQL / Relational Database Platforms

## 2.1 Supabase

**Assessment: Strong candidate**

### Free allowance

| Resource | Free allowance |
|---|---:|
| PostgreSQL database | 500 MB |
| Egress | 5 GB |
| Cached egress | 5 GB |
| File storage | 1 GB |
| Active free projects | 2 |

### Advantages

- Provides a managed PostgreSQL database.
- Supports conventional PostgreSQL connections.
- Works with Python libraries such as `psycopg` and SQLAlchemy.
- Includes a database dashboard and SQL editor.
- Provides REST and GraphQL APIs.
- Offers authentication and file storage if needed.
- Supports connection pooling.

### Limitations

- Free projects pause after approximately one week of insufficient activity.
- Database storage is limited to 500 MB.
- Free projects use shared compute resources.
- The free plan does not include the same backup capabilities as paid plans.
- Direct PostgreSQL connections use IPv6 by default; the shared pooler provides an IPv4 connection option.

### Assessment

Supabase is more than a database provider. It offers several backend services that could be useful for a larger application.

However, this project does not necessarily need its authentication, storage, or API features. The Python backend can communicate directly with its PostgreSQL database.

The inactivity pause is inconvenient, but the database can be resumed.

**Verdict:** Recommended. Particularly useful if the dashboard eventually needs authentication or additional backend services.

### Sources

- https://supabase.com/pricing
- https://supabase.com/docs/guides/platform/free-project-pausing
- https://supabase.com/docs/guides/database/connecting-to-postgres

---

## 2.2 Neon

**Assessment: Very strong candidate**

### Free allowance

| Resource | Free allowance |
|---|---:|
| PostgreSQL storage | 1 GB per project |
| Compute | 100 CU-hours per project/month |
| Maximum autoscaling | 2 CU |
| Branches | 10 per project |
| Projects | 100 |
| Public network transfer | 5 GB per project/month |

### Advantages

- Provides managed PostgreSQL.
- Compatible with conventional PostgreSQL tools and Python libraries.
- Automatically scales compute based on demand.
- Compute scales to zero after inactivity.
- Supports database branching.
- Provides a six-hour instant restore window.
- Can be used independently of the hosting provider.

### Limitations

- Compute scales to zero after approximately five minutes of inactivity.
- The first query after inactivity may experience additional latency.
- The free plan has a monthly compute allowance.
- Storage and network transfer are limited.
- The instant restore window is not equivalent to a long-term backup strategy.

### Assessment

Neon is particularly suitable for a small dashboard.

A daily synchronization process and occasional website requests should require relatively little database compute.

The 1 GB storage allowance is also twice Supabase's free database allowance.

The main inconvenience is the scale-to-zero behavior. The first database request after a period of inactivity may take longer.

**Verdict:** Strongest overall PostgreSQL candidate for this project.

### Sources

- https://neon.com/blog/neon-free-plan-1-gb-per-project
- https://neon.com/docs

---

## 2.3 Turso

**Assessment: Good database, but not the preferred database type**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Storage | 5 GB |
| Rows read | 500 million/month |
| Rows written | 10 million/month |
| Databases | 100 |
| Monthly sync transfer | 3 GB |
| Point-in-time restore | 1 day |

### Advantages

- Generous free storage allowance.
- High read and write quotas.
- Designed for distributed database workloads.
- Supports SQL queries.
- Lightweight database architecture.
- Can be useful for applications that benefit from SQLite compatibility.

### Limitations

- Uses SQLite/libSQL rather than PostgreSQL.
- Not a drop-in replacement for a PostgreSQL database.
- Requires a different database driver and potentially different ORM configuration.
- Some PostgreSQL-specific features and SQL behavior will not transfer directly.
- Switching database providers later may require migration work.

### Assessment

Turso's free allowance is generous, especially for a relatively small application.

However, storage capacity is not the main concern here. The project benefits more from using a conventional PostgreSQL database that integrates naturally with the planned Python backend.

**Verdict:** Not recommended unless there is a specific reason to use SQLite/libSQL.

### Source

- https://turso.tech/pricing

---

## 2.4 Cloudflare D1

**Assessment: Good for Cloudflare-based applications**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Storage | 5 GB total |
| Rows read | 5 million/day |
| Rows written | 100,000/day |

### Advantages

- Serverless SQL database.
- SQLite-compatible SQL.
- Generous free storage and query allowances.
- No database compute-hour charge.
- Supports foreign-key relationships.
- Integrates directly with Cloudflare Workers.
- Includes database recovery capabilities.

### Limitations

- Uses SQLite semantics rather than PostgreSQL.
- Designed primarily for Cloudflare Workers and Pages.
- Native integration uses Cloudflare database bindings.
- Does not provide a conventional PostgreSQL connection string.
- Using it from a separate conventional FastAPI backend requires a different integration approach, such as its HTTP API.
- SQL compatibility and application behavior differ from PostgreSQL.

### Assessment

D1 is attractive if the entire application is built around Cloudflare Workers.

However, the intended architecture uses a conventional Python backend. Using D1 would introduce additional integration decisions without providing a significant advantage for this project.

**Verdict:** Eliminate from the primary shortlist.

### Sources

- https://developers.cloudflare.com/d1/platform/pricing/
- https://developers.cloudflare.com/d1/best-practices/query-d1/
- https://developers.cloudflare.com/d1/

---

## 2.5 Firebase Firestore

**Assessment: Not recommended for this project**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Stored data | 1 GiB |
| Document reads | 50,000/day |
| Document writes | 20,000/day |
| Document deletes | 20,000/day |
| Outbound transfer | 10 GiB/month |

### Advantages

- Managed NoSQL database.
- Generous free daily read and write quotas.
- Supports real-time updates.
- Integrates with Firebase authentication and other services.
- Useful for applications with flexible document structures.

### Limitations

- NoSQL rather than relational SQL.
- Data is organized into collections and documents.
- Relational queries and joins require a different approach.
- Data modeling differs from PostgreSQL.
- Some additional features, including backups and point-in-time recovery, require billing.

### Assessment

Firestore is useful for applications that benefit from document-based data structures and real-time synchronization.

However, this dashboard has structured project information and relationships between records.

A relational database is a more natural fit.

**Verdict:** Eliminate unless the project changes toward a document-oriented architecture.

### Sources

- https://firebase.google.com/docs/firestore/quotas
- https://firebase.google.com/docs/firestore/pricing

---

## 2.6 Render PostgreSQL

**Assessment: Suitable for testing, not long-term storage**

### Free allowance

| Resource | Free allowance |
|---|---:|
| PostgreSQL storage | 1 GB |
| Active free databases | 1 per workspace |
| Database lifetime | 30 days |

### Advantages

- Conventional PostgreSQL.
- Convenient integration with Render-hosted Python services.
- Simple deployment and connection configuration.
- Suitable for development and temporary demonstrations.

### Limitations

- Free databases expire 30 days after creation.
- No free database backups.
- Database availability may be interrupted by maintenance or restarts.
- Expired databases eventually become inaccessible and are deleted unless upgraded.

### Assessment

Render PostgreSQL is convenient when the backend is also hosted on Render.

However, the 30-day expiration makes it unsuitable as the permanent database for this dashboard.

A database that periodically expires defeats the purpose of persistent storage.

**Verdict:** Use only for temporary testing. Do not use as the main database.

### Sources

- https://render.com/docs/free
- https://render.com/changelog/free-postgresql-instances-now-expire-after-30-days-previously-90

---

# 3. Overall Comparison

| Platform | Database Type | Free Storage | Main Limitation | Verdict |
|---|---|---:|---|---|
| Neon | PostgreSQL | 1 GB/project | Compute scales to zero | Recommended |
| Supabase | PostgreSQL | 500 MB/project | Pauses after inactivity | Recommended |
| Turso | SQLite/libSQL | 5 GB | Not PostgreSQL | Alternative |
| Cloudflare D1 | SQLite-compatible SQL | 5 GB total | Cloudflare-oriented integration | Low priority |
| Firebase Firestore | NoSQL | 1 GiB | Not relational SQL | Eliminate |
| Render PostgreSQL | PostgreSQL | 1 GB | Expires after 30 days | Testing only |

---

# 4. Neon vs. Supabase

These are the two strongest candidates because both provide conventional PostgreSQL.

| Category | Neon | Supabase |
|---|---|---|
| Database | PostgreSQL | PostgreSQL |
| Free storage | 1 GB | 500 MB |
| Compute model | Serverless | Shared compute |
| Inactivity behavior | Scales to zero | Project pauses |
| Python compatibility | Yes | Yes |
| SQLAlchemy compatibility | Yes | Yes |
| Database branching | Yes | Not the primary focus |
| Additional backend services | Auth, storage, functions | Auth, storage, APIs, functions |
| Best use | Standalone PostgreSQL | Integrated backend platform |

## Neon advantages

- Twice the free database storage.
- Database can be used independently of the backend host.
- Compute scales automatically.
- Database branching is useful for experimentation.
- Straightforward PostgreSQL integration.

## Supabase advantages

- More integrated backend functionality.
- Built-in database dashboard and SQL editor.
- REST and GraphQL APIs.
- Authentication and file storage.
- Useful if the project expands beyond a simple dashboard.

## Decision

For the current architecture, Neon is the better starting point.

Supabase becomes more attractive if the project eventually needs authentication, file storage, or additional backend services.

---

# 5. Recommended Database Architecture

Use PostgreSQL as the persistent storage layer.

The database should contain a synchronized representation of Notion data rather than replace Notion as the original source of truth.

```text
                   NOTION
               Source of Truth
                      |
                      v
               PYTHON BACKEND
                   FastAPI
                      |
                Notion API
                      |
                      v
                  NEON
                PostgreSQL
                      |
                 SQL Queries
                      |
                      v
               PYTHON BACKEND
                      |
                 REST API
                      |
                      v
               REACT FRONTEND
                  Dashboard
```

## Suggested initial tables

| Table | Purpose |
|---|---|
| `projects` | Stores project information |
| `tasks` | Stores tasks associated with projects |
| `categories` | Stores project categories |
| `sync_logs` | Tracks synchronization attempts |
| `settings` | Stores application-level settings if needed |

The schema should reflect the actual Notion database structure. Avoid creating unnecessary tables before the requirements are clear.

## Important implementation decisions

1. Store the original Notion page ID in each synchronized record.
2. Use the Notion page ID as a stable external identifier.
3. Use `created_at` and `updated_at` timestamps.
4. Make synchronization idempotent.
5. Use database transactions when updating related records.
6. Track the last successful synchronization.
7. Handle deleted or archived Notion records.
8. Keep database credentials on the backend.
9. Do not let the React frontend connect directly to PostgreSQL.
10. Maintain a backup or export strategy.

---

# 6. Final Recommendation

**Primary choice: Neon PostgreSQL**

Recommended order:

1. **Neon:** Best overall fit for the current project.
2. **Supabase:** Best alternative if additional backend services are needed.
3. **Turso:** Consider only if SQLite/libSQL becomes preferable.
4. **Cloudflare D1:** Consider if the application moves to Cloudflare Workers.
5. **Firebase Firestore:** Not suitable for the preferred relational architecture.
6. **Render PostgreSQL:** Use for temporary testing only.

## Suggested combination

| Component | Recommended Platform |
|---|---|
| Frontend | Vercel or another static hosting provider |
| Python backend | Render, Koyeb, or Vercel |
| Database | Neon PostgreSQL |
| Source of truth | Notion |
| Automatic synchronization | Backend scheduler or external scheduler |

The database does not need to be hosted by the same provider as the Python backend.

Keeping Neon independent makes it easier to change backend hosting later without migrating the database.

---

# 7. Next Steps

Before committing to Neon:

1. Create a small PostgreSQL database.
2. Connect to it from the FastAPI backend.
3. Test inserting and retrieving project records.
4. Test updating an existing record without creating duplicates.
5. Test the connection after the database scales to zero.
6. Test the database connection from the intended hosting provider.
7. Verify that the free compute and transfer allowances are sufficient.
8. Establish a database export or backup procedure.

**Do not select a database based on storage capacity alone.** For this project, compatibility, persistence, connection reliability, and portability are more important than having several additional gigabytes.

---

# 8. Sources

## Supabase
- [Supabase Pricing](https://supabase.com/pricing)
- [Free Project Pausing](https://supabase.com/docs/guides/platform/free-project-pausing)
- [Connecting to PostgreSQL](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres/pooling-and-limits)

## Neon
- [Neon Free Plan Update — October 2, 2026](https://neon.com/blog/neon-free-plan-1-gb-per-project)
- [Neon Documentation](https://neon.com/docs)

## Turso
- [Turso Pricing](https://turso.tech/pricing)

## Cloudflare D1
- [D1 Pricing](https://developers.cloudflare.com/d1/platform/pricing/)
- [Querying D1](https://developers.cloudflare.com/d1/best-practices/query-d1/)
- [D1 Documentation](https://developers.cloudflare.com/d1/)

## Firebase
- [Firestore Quotas and Limits](https://firebase.google.com/docs/firestore/quotas)
- [Firestore Pricing](https://firebase.google.com/docs/firestore/pricing)

## Render
- [Render Free Services and Databases](https://render.com/docs/free)
- [Free PostgreSQL Expiration Announcement](https://render.com/changelog/free-postgresql-instances-now-expire-after-30-days-previously-90)

---

**Assessment note:** Free-tier quotas, regional availability, and pricing can change. Verify the current terms before deployment.


#### Neon

An excellent alternative to Supabase.

-   Its October 2026 free plan includes 1 GB of database storage per
    project.
-   Includes 100 CU-hours.
-   Compute scales to zero after inactivity.

#### Supabase

An excellent all-in-one backend database.

-   Offers PostgreSQL, authentication, storage, and APIs.
-   Its free plan has a 500 MB database allowance and two active
    projects.
-   Free projects pause after a week of inactivity.

### B. NoSQL Databases

  Platform             Free possibility         Best use
  -------------------- ------------------------ ----------------------------
  MongoDB Atlas        512 MB free cluster      Document-oriented data
  Firebase Firestore   Daily free quotas        Real-time application data
  Upstash Redis        Limited free allowance   Caching and temporary data

MongoDB Atlas has a 512 MB free cluster with operational limits, while
Firestore has daily read/write quotas.

**Database preference: PostgreSQL.**

Project records have predictable properties: name, description, status,
dates, categories, technologies, and links. Relational SQL fits this
structure naturally.

------------------------------------------------------------------------

## 4. Scheduling and Automation Platforms

Scheduling matters because the project needs automatic synchronization
every day. The scheduler does not necessarily need to be hosted by the
same provider as the Python backend.

  -----------------------------------------------------------------------
  Platform                Free possibility        Can trigger your Python
                                                  API?
  ----------------------- ----------------------- -----------------------
  GitHub Actions          2,000 minutes/month on  Yes
                          GitHub Free private     
                          repos; standard runners 
                          free for public repos   

  Vercel Cron             Daily scheduling on     Yes, through HTTP
                          Hobby                   

  Cloudflare Cron         Included in Workers     Yes, through HTTP
  Triggers                Free limits             

  Google Cloud Scheduler  3 jobs per billing      Yes
                          account                 

  Render Cron Jobs        No free cron compute    Yes, but minimum
                                                  \$1/month per cron
                                                  service

  Netlify Scheduled       Uses free-plan credits  Yes
  Functions                                       

  AWS EventBridge         Limited free allowance  Yes
  Scheduler                                       

  Azure Functions Timer   Uses Functions free     Yes
  Trigger                 grant                   

  PythonAnywhere Tasks    No scheduled tasks on   Not on the free tier
                          Beginner                
  -----------------------------------------------------------------------


# Scheduling and Automation Platform Assessment

**Project:** Notion Project Dashboard  
**Assessment Date:** November 7, 2026

---

# 1. Project Requirements

The dashboard requires automatic synchronization between Notion and PostgreSQL.

The synchronization process should:

- Run automatically once per day.
- Retrieve updated information from Notion.
- Insert or update records in PostgreSQL.
- Record synchronization status and timestamps.
- Handle failed requests without corrupting existing data.
- Work even when the website is not being visited.
- Ideally cost ₱0.

The project also requires a manual synchronization button.

## Recommended synchronization architecture

The scheduler should trigger an endpoint exposed by the Python backend.

```text
                 SCHEDULER
              (Daily Trigger)
                     |
                     | HTTP Request
                     v
              PYTHON BACKEND
                  FastAPI
                     |
                     v
              SYNC ENDPOINT
              /api/sync/notion
                     |
                     v
                 NOTION API
                     |
                     v
                PostgreSQL
                     |
                     v
              React Dashboard
```

The manual synchronization button should call the same backend synchronization endpoint.

```text
        AUTOMATIC SYNC             MANUAL SYNC
        (Daily Scheduler)         (Website Button)
                |                        |
                v                        v
          HTTP Request             HTTP Request
                |                        |
                +-----------+------------+
                            |
                            v
                     FastAPI Backend
                            |
                            v
                      Sync Process
                            |
                            v
                       PostgreSQL
```

This avoids maintaining two separate synchronization implementations.

---

# 2. Scheduling and Automation Platforms

## 2.1 GitHub Actions

**Assessment: Strongest overall candidate**

### Free allowance

| Resource | Free allowance |
|---|---:|
| GitHub Free private repositories | 2,000 minutes/month |
| Public repository standard runners | Free |
| Scheduled workflows | Supported |
| Minimum scheduling interval | 5 minutes |

### Advantages

- Works independently of the backend hosting provider.
- Supports scheduled workflows using cron expressions.
- Can send HTTP requests to the FastAPI backend.
- Can execute Python scripts directly if necessary.
- Supports repository secrets for API credentials.
- Integrates directly with GitHub repositories.
- No separate server is required.

### Limitations

- Private repositories consume the monthly Actions allowance.
- Public repositories have their own scheduling restrictions.
- Scheduled workflows can be delayed during periods of high platform activity.
- Public repositories automatically disable scheduled workflows after 60 days without repository activity.
- Scheduled workflows run using the latest commit on the default branch.
- Requires the workflow file to be maintained in the repository.

### Assessment

GitHub Actions is particularly suitable because the project already uses GitHub for source control.

A workflow can execute once per day and send an authenticated HTTP request to the FastAPI synchronization endpoint.

For example:

```text
GitHub Actions
      |
      | POST /api/sync/notion
      v
FastAPI Backend
      |
      v
Notion API
      |
      v
Neon PostgreSQL
```

A daily synchronization request should consume very little of the monthly execution allowance.

Even a workflow that takes two minutes per day would use approximately 60 minutes per month, well below the 2,000-minute private repository allowance.

The main disadvantage is scheduling reliability: GitHub documents that scheduled workflows can be delayed during high-load periods.

For a dashboard that only needs daily synchronization, this is generally acceptable.

**Verdict:** Best overall option. Recommended as the primary scheduler.

### Sources

- https://github.com/pricing
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

---

## 2.2 Vercel Cron

**Assessment: Strong candidate**

### Free allowance

| Resource | Free allowance |
|---|---|
| Cron availability | Available on all plans |
| Hobby scheduling | Once per day |
| Scheduling accuracy | Any time within the specified hour |
| Trigger method | HTTP request to a Vercel Function |

### Advantages

- Convenient if the frontend or backend is hosted on Vercel.
- Supports cron expressions.
- Can trigger a backend function through HTTP.
- Supports environment variables for secrets.
- Provides execution logs.
- Requires little infrastructure configuration.

### Limitations

- Hobby users can schedule a cron job only once per day.
- Execution may happen at any point within the scheduled hour.
- Cron jobs run in UTC.
- Vercel Cron is designed to invoke Vercel Functions.
- Function execution limits still apply.

### Assessment

Vercel Cron is an excellent choice if the dashboard's backend is also deployed on Vercel.

For example:

```text
Vercel Cron
     |
     v
/api/sync/notion
     |
     v
FastAPI Function
     |
     v
Neon PostgreSQL
```

However, if the Python backend is hosted on Render or Koyeb, GitHub Actions provides a more hosting-independent solution.

Vercel's once-per-day restriction is not a problem for this project.

The execution window means the synchronization should not depend on running at an exact minute.

**Verdict:** Recommended if Vercel hosts the backend. Otherwise, GitHub Actions is more flexible.

### Sources

- https://vercel.com/docs/cron-jobs
- https://vercel.com/docs/cron-jobs/manage-cron-jobs
- https://vercel.com/pricing

---

## 2.3 Cloudflare Cron Triggers

**Assessment: Good for Cloudflare-based applications**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Cron Triggers | 5 per account |
| Cron CPU time | 10 ms per invocation |
| Worker memory | 128 MB |
| Worker requests | 100,000/day |

### Advantages

- Included in Cloudflare Workers.
- Supports scheduled execution through cron expressions.
- Can make HTTP requests using the Worker's `fetch()` API.
- Does not require a separate conventional server.
- Useful for applications already deployed on Cloudflare.
- Supports multiple scheduled triggers within the account limit.

### Limitations

- Cron execution runs inside a Cloudflare Worker.
- Free Cron Triggers have a 10 ms CPU-time limit.
- The Python runtime and its package compatibility must be considered if using Python Workers.
- Cron expressions use UTC.
- Requires Cloudflare-specific configuration.

### Assessment

Cloudflare Cron Triggers can execute a Worker that sends an HTTP request to the FastAPI backend.

For example:

```text
Cloudflare Cron Trigger
          |
          v
     Cloudflare Worker
          |
          | fetch()
          v
     FastAPI Backend
          |
          v
      Notion API
          |
          v
    Neon PostgreSQL
```

The scheduler itself does not need to run the entire synchronization process.

It can simply make one authenticated request to the existing backend.

This reduces the amount of work performed inside the Worker and makes the CPU limit less concerning.

**Verdict:** Good alternative if Cloudflare is already part of the application architecture. Not necessary otherwise.

### Sources

- https://developers.cloudflare.com/workers/configuration/cron-triggers/
- https://developers.cloudflare.com/workers/platform/limits/
- https://developers.cloudflare.com/workers/platform/pricing/

---

## 2.4 Google Cloud Scheduler

**Assessment: Strong technical candidate**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Jobs | 3 per billing account |
| Additional jobs | $0.10/job per 31 days |
| HTTP targets | Supported |
| Scheduling | Cron expressions |

### Advantages

- Supports direct HTTP requests.
- Supports authenticated HTTP targets.
- Can use OIDC tokens for authentication.
- Supports cron expressions and timezone configuration.
- Independent of the Python backend's hosting provider.
- Integrates naturally with Google Cloud Run.

### Limitations

- Requires a Google Cloud billing account.
- Requires additional Google Cloud configuration.
- Requires setting up a service account for authenticated requests.
- Other Google Cloud services may introduce charges.
- More setup than GitHub Actions.

### Assessment

Google Cloud Scheduler is one of the most straightforward dedicated scheduling services.

Unlike some alternatives, it can directly send an HTTP request to an external HTTPS endpoint.

It also supports OIDC authentication, which is preferable to placing a secret directly in a URL.

Example:

```text
Google Cloud Scheduler
          |
          | Authenticated HTTP Request
          v
     FastAPI Backend
          |
          v
     Notion API
          |
          v
    Neon PostgreSQL
```

Three free jobs are more than enough for this project.

However, the requirement to configure a Google Cloud billing account makes it less convenient than GitHub Actions.

**Verdict:** Recommended if the backend is hosted on Google Cloud Run or if a dedicated scheduler is preferred.

### Sources

- https://cloud.google.com/scheduler/pricing
- https://docs.cloud.google.com/scheduler/docs/http-target-auth
- https://cloud.google.com/scheduler/docs

---

## 2.5 Render Cron Jobs

**Assessment: Technically suitable, but not free**

### Free allowance

| Resource | Allowance |
|---|---|
| Cron job service | No free compute |
| Minimum monthly charge | $1 per cron service |
| Billing | Based on active execution time, subject to minimum charge |
| Scheduling | Cron expressions |

### Advantages

- Can execute Python scripts directly.
- Supports environment variables.
- Integrates with Render services.
- Provides execution logs.
- Supports scheduled tasks.
- Does not require a separate external scheduler.

### Limitations

- No free cron compute.
- Minimum monthly charge is $1 per cron service.
- Cannot access persistent disks.
- Requires a separate cron service from the web service.

### Assessment

Render Cron Jobs are convenient if the backend is also hosted on Render.

The cron job can execute a Python synchronization script directly instead of making an HTTP request.

However, the minimum monthly charge makes it unsuitable for the project's ₱0 target.

GitHub Actions can perform a similar scheduling function without this additional hosting cost.

**Verdict:** Eliminate for the free-tier architecture.

### Sources

- https://render.com/docs/cronjobs
- https://render.com/pricing

---

## 2.6 Netlify Scheduled Functions

**Assessment: Possible, but unnecessary**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Monthly credits | 300 |
| Compute | 10 credits/GB-hour |
| Web requests | 2 credits/10,000 requests |
| Scheduled Functions | Available on all plans |
| Execution limit | 30 seconds |

### Advantages

- Scheduled Functions are available on the free plan.
- Supports cron expressions.
- Can execute code on a schedule.
- Can make HTTP requests to an external backend.
- Provides execution logs.
- Useful if the frontend is hosted on Netlify.

### Limitations

- Uses the Netlify Functions execution environment.
- Scheduled Functions have a 30-second execution limit.
- Scheduled Functions run in UTC.
- Scheduled Functions cannot be invoked directly through a URL.
- Free usage is governed by a monthly credit allowance.
- The free plan has a hard usage limit.

### Assessment

Netlify Scheduled Functions are useful for triggering external services.

However, the scheduled function itself must be implemented and deployed on Netlify. It cannot simply be configured as a URL-based cron service.

A small JavaScript function could send an HTTP request to the Python backend.

For example:

```text
Netlify Scheduled Function
          |
          | HTTP Request
          v
     FastAPI Backend
          |
          v
     Notion API
          |
          v
    Neon PostgreSQL
```

This is possible, but GitHub Actions provides the same functionality with fewer platform-specific dependencies.

**Verdict:** Low priority. Consider only if Netlify is already being used.

### Sources

- https://docs.netlify.com/build/functions/scheduled-functions/
- https://www.netlify.com/pricing/
- https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/

---

## 2.7 AWS EventBridge Scheduler

**Assessment: Good for AWS-based applications**

### Free allowance

| Resource | Free allowance |
|---|---:|
| Scheduler invocations | 14 million/month |
| Cron scheduling | Supported |
| Retry policies | Supported |
| Dead-letter queues | Supported |

### Advantages

- Highly scalable scheduling service.
- Supports recurring cron and rate schedules.
- Supports retry policies.
- Supports dead-letter queues.
- Integrates with AWS Lambda.
- Generous free invocation allowance.

### Limitations

- Does not directly support arbitrary external HTTP endpoints as native Scheduler targets.
- Typically requires an AWS Lambda function to call the external FastAPI endpoint.
- Requires IAM roles and permissions.
- More complicated than GitHub Actions.
- Other AWS services may introduce additional charges.

### Assessment

EventBridge Scheduler is capable of scheduling the synchronization process.

However, there is an important distinction: EventBridge Scheduler primarily targets AWS services.

For an external FastAPI backend, a typical architecture would be:

```text
EventBridge Scheduler
          |
          v
       AWS Lambda
          |
          | HTTP Request
          v
     FastAPI Backend
          |
          v
     Notion API
          |
          v
    Neon PostgreSQL
```

The Lambda function introduces another component that must be configured and maintained.

AWS EventBridge is more attractive when the backend is already hosted within AWS.

**Verdict:** Technically suitable, but unnecessary complexity for this project.

### Sources

- https://aws.amazon.com/eventbridge/pricing/
- https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html
- https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-custom-bus-target-http.html

---

## 2.8 Azure Functions Timer Trigger

**Assessment: Technically suitable, but low priority**

### Free allowance

The newer Flex Consumption plan provides:

| Resource | Free allowance |
|---|---:|
| Executions | 250,000/month |
| Compute | 100,000 GB-seconds/month |
| Scheduling | Timer Trigger supported |

These grants apply to eligible pay-as-you-go subscriptions and on-demand usage. Storage and networking may be billed separately.

### Advantages

- Supports Python.
- Supports scheduled execution through Timer Triggers.
- Can execute code without maintaining a continuously running server.
- Can make HTTP requests to external services.
- Integrates with other Azure services.

### Limitations

- Requires an Azure Functions application.
- Timer Trigger executes code inside the Azure Function rather than directly calling an external URL.
- Additional configuration is necessary.
- Storage costs are separate from the free compute grant.
- Free allowances depend on the hosting plan and subscription.

### Assessment

Azure Functions can run a scheduled Python function that calls the FastAPI synchronization endpoint.

However, this introduces another application and another hosting platform.

There is little benefit to adding Azure infrastructure when GitHub Actions can already perform the daily request.

**Verdict:** Not recommended unless the application already uses Azure.

### Sources

- https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale
- https://learn.microsoft.com/en-us/azure/azure-functions/pricing
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer

---

## 2.9 PythonAnywhere Scheduled Tasks

**Assessment: Not suitable for a new free account**

### Free allowance

| Resource | Free allowance |
|---|---|
| Beginner plan | No scheduled tasks for newly created free accounts |
| Paid plans | Scheduled tasks available |
| Legacy free accounts | One daily task for accounts created before January 15, 2026, subject to regional cutoff |

### Advantages

- Designed specifically for Python.
- Supports scheduled Python scripts on eligible plans.
- Can execute synchronization code directly.
- Does not require a separate cron implementation.

### Limitations

- Newly created free accounts do not receive scheduled tasks.
- Paid plans are required for new users who need scheduled execution.
- Free accounts have restricted outbound internet access.
- Not useful as a free external scheduler for this architecture.

### Assessment

PythonAnywhere would be convenient if the backend itself were hosted there and the account had scheduled-task access.

However, its current free-account restrictions make it unsuitable for this project.

**Verdict:** Eliminate for the free-tier architecture.

### Sources

- https://help.pythonanywhere.com/pages/ScheduledTasks/
- https://www.pythonanywhere.com/pricing/

---

# 3. Overall Comparison

| Platform | Free Scheduling | Can Trigger External API? | Main Limitation | Verdict |
|---|---|---|---|---|
| GitHub Actions | 2,000 minutes/month for private repos; public standard runners free | Yes, directly | Possible scheduling delays | Recommended |
| Vercel Cron | Daily on Hobby | Yes, through Vercel Functions | Once daily; hourly execution window | Recommended |
| Cloudflare Cron | 5 triggers/account | Yes, through Worker `fetch()` | 10 ms free CPU limit | Recommended for Cloudflare |
| Google Cloud Scheduler | 3 free jobs/account | Yes, directly | Billing account required | Recommended |
| Render Cron Jobs | No free compute | Yes, or run Python directly | $1/month minimum | Eliminate |
| Netlify Scheduled Functions | 300 monthly credits | Yes, through function code | 30-second execution limit | Low priority |
| AWS EventBridge Scheduler | 14 million invocations/month | Through Lambda or API Destinations | AWS configuration | Alternative |
| Azure Functions Timer | Free grant on eligible plan | Through function code | Additional infrastructure | Low priority |
| PythonAnywhere | No tasks for new free accounts | Not on the new free tier | Paid plan required | Eliminate |

---

# 4. Comparison of the Strongest Candidates

## GitHub Actions vs. Vercel Cron vs. Google Cloud Scheduler

These are the most practical options for the current architecture.

| Category | GitHub Actions | Vercel Cron | Google Cloud Scheduler |
|---|---|---|---|
| Free usage | 2,000 minutes/month on Free private repos | Daily on Hobby | 3 jobs/account |
| Direct HTTP request | Yes | Through Vercel Function | Yes |
| Backend hosting dependency | None | Best with Vercel | None |
| Timezone support | UTC or configured timezone | UTC | Configurable timezone |
| Authentication | Repository secrets | Environment variables | OIDC/service account |
| Setup complexity | Low | Low | Medium |
| Best use | General-purpose scheduler | Vercel applications | Dedicated HTTP scheduler |

## GitHub Actions advantages

- Works with almost any backend host.
- No need to deploy another function.
- Easy to maintain in the existing repository.
- Suitable for daily API calls.
- No separate scheduler subscription.

## Vercel Cron advantages

- Convenient if Vercel already hosts the application.
- Minimal additional infrastructure.
- Integrated execution logs.
- Simple environment variable configuration.

## Google Cloud Scheduler advantages

- Dedicated scheduling service.
- Direct authenticated HTTP requests.
- Configurable timezone.
- More appropriate if precise scheduling and managed service reliability are important.

## Decision

For the current project, GitHub Actions is the most practical choice.

Google Cloud Scheduler is the strongest dedicated scheduling alternative.

Vercel Cron becomes more attractive if Vercel is selected as the backend hosting provider.

---

# 5. Recommended Architecture

## Recommended combination

| Component | Recommended Platform |
|---|---|
| Source of truth | Notion |
| Python backend | Render, Koyeb, or Vercel |
| Database | Neon PostgreSQL |
| Frontend | Vercel or another static host |
| Daily scheduler | GitHub Actions |
| Manual synchronization | React frontend calling FastAPI |

## Daily synchronization flow

```text
             GITHUB ACTIONS
               Daily Trigger
                     |
                     |
                     v
             Authenticated Request
                     |
                     v
               FASTAPI BACKEND
                     |
                     v
                NOTION API
                     |
                     v
               NEON POSTGRES
                     |
                     v
              SYNC LOG UPDATED
```

## Manual synchronization flow

```text
              REACT DASHBOARD
                     |
                     |
                Sync Button
                     |
                     v
              FASTAPI BACKEND
                     |
                     v
                NOTION API
                     |
                     v
               NEON POSTGRES
                     |
                     v
              SYNC LOG UPDATED
```

Both flows should use the same synchronization implementation.

---

# 6. Important Implementation Considerations

## 6.1 Secure the synchronization endpoint

Do not leave the synchronization endpoint publicly accessible without authentication.

The scheduler should provide a secret or authenticated token.

For example:

```http
POST /api/sync/notion
Authorization: Bearer <SYNC_SECRET>
```

Store the secret in:

- GitHub Actions repository secrets.
- Backend environment variables.

Never commit the secret to GitHub or expose it in React.

For Google Cloud Scheduler, OIDC authentication is preferable when supported by the receiving backend.

## 6.2 Prevent duplicate synchronization

A manual request and automatic request could happen at the same time.

The backend should prevent concurrent synchronization jobs from interfering with each other.

Possible solutions:

- Database advisory locks.
- A synchronization status record.
- A dedicated job-lock table.

The synchronization process should also be idempotent.

Running the same synchronization twice should not create duplicate projects or tasks.

## 6.3 Track synchronization status

A `sync_logs` table can record:

| Field | Purpose |
|---|---|
| `id` | Synchronization record ID |
| `started_at` | Start timestamp |
| `completed_at` | Completion timestamp |
| `status` | Success, failed, or running |
| `records_created` | Number of new records |
| `records_updated` | Number of updated records |
| `error_message` | Error information, if any |
| `trigger_source` | Manual or scheduled |

This makes it possible to show the last successful synchronization on the dashboard.

## 6.4 Handle failed synchronization

The backend should:

1. Record the start of synchronization.
2. Retrieve Notion records.
3. Process pagination.
4. Validate the retrieved data.
5. Insert or update PostgreSQL records.
6. Commit database changes safely.
7. Record success or failure.
8. Return an appropriate HTTP response.

Do not mark synchronization as successful if only part of the process completed.

## 6.5 Choose an appropriate timezone

The project is being developed in the Philippines.

The desired timezone is:

```text
Asia/Manila
UTC+08:00
```

Some schedulers use UTC by default.

For example:

```text
01:00 UTC = 09:00 Asia/Manila
```

GitHub Actions supports timezone-aware scheduling. Vercel, Cloudflare, and Netlify use UTC for their cron schedules.

## 6.6 Avoid unnecessary synchronization

The scheduler only needs to run once per day.

There is no reason to synchronize every few minutes unless the project later requires near-real-time updates.

---

# 7. Final Recommendation

**Primary choice: GitHub Actions**

Recommended ranking:

1. **GitHub Actions:** Best overall option for this project.
2. **Vercel Cron:** Best if the backend is hosted on Vercel.
3. **Google Cloud Scheduler:** Best dedicated external HTTP scheduler.
4. **Cloudflare Cron Triggers:** Best if using Cloudflare Workers.
5. **AWS EventBridge Scheduler:** Good if the application uses AWS.
6. **Azure Functions Timer:** Suitable, but unnecessary infrastructure.
7. **Netlify Scheduled Functions:** Possible, but less convenient.
8. **Render Cron Jobs:** Not free.
9. **PythonAnywhere:** Not suitable for newly created free accounts.

## Why GitHub Actions?

The project already uses GitHub for source control.

GitHub Actions can:

- Run once every day.
- Call the FastAPI synchronization endpoint.
- Store the synchronization secret securely.
- Operate independently of the backend host.
- Stay within the free monthly allowance for a small daily workflow.

It also avoids adding another cloud provider solely for scheduling.

---

# 8. Suggested Next Steps

Before finalizing the scheduler:

1. Deploy the FastAPI backend.
2. Create and test the synchronization endpoint.
3. Add authentication to the endpoint.
4. Test manual synchronization from React.
5. Create a GitHub Actions workflow.
6. Configure the workflow to run once per day.
7. Add the synchronization secret to GitHub Actions.
8. Test the scheduled request manually.
9. Confirm that synchronization logs are recorded in PostgreSQL.
10. Test failure handling and duplicate-run prevention.

The scheduler should be selected after the backend endpoint is working.

**The scheduler is only responsible for starting synchronization. The Python backend remains responsible for the actual synchronization logic.**

---

# 9. Sources

## GitHub Actions

- [GitHub Pricing](https://github.com/pricing)
- [GitHub Actions Billing and Usage](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [Workflow Events and Scheduled Triggers](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [Troubleshooting Scheduled Workflows](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows)

## Vercel Cron

- [Vercel Cron Jobs](https://vercel.com/docs/cron-jobs)
- [Managing Cron Jobs](https://vercel.com/docs/cron-jobs/manage-cron-jobs)
- [Vercel Pricing](https://vercel.com/pricing)

## Cloudflare Cron

- [Cron Triggers](https://developers.cloudflare.com/workers/configuration/cron-triggers/)
- [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)
- [Workers Pricing](https://developers.cloudflare.com/workers/platform/pricing/)

## Google Cloud Scheduler

- [Cloud Scheduler Pricing](https://cloud.google.com/scheduler/pricing)
- [HTTP Target Authentication](https://docs.cloud.google.com/scheduler/docs/http-target-auth)
- [Cloud Scheduler Documentation](https://cloud.google.com/scheduler/docs)

## Render Cron Jobs

- [Render Cron Jobs](https://render.com/docs/cronjobs)
- [Render Pricing](https://render.com/pricing)

## Netlify Scheduled Functions

- [Scheduled Functions Documentation](https://docs.netlify.com/build/functions/scheduled-functions/)
- [Netlify Pricing](https://www.netlify.com/pricing/)
- [How Credits Work](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)

## AWS EventBridge Scheduler

- [EventBridge Pricing](https://aws.amazon.com/eventbridge/pricing/)
- [Invoke Lambda on a Schedule](https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html)
- [EventBridge Scheduler Targets](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets.html)
- [HTTP Targets and API Destinations](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-custom-bus-target-http.html)

## Azure Functions

- [Azure Functions Hosting Options](https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale)
- [Azure Functions Pricing](https://learn.microsoft.com/en-us/azure/azure-functions/pricing)
- [Timer Trigger Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer)

## PythonAnywhere

- [Scheduled Tasks](https://help.pythonanywhere.com/pages/ScheduledTasks/)
- [PythonAnywhere Pricing](https://www.pythonanywhere.com/pricing/)

---

**Assessment note:** Free-tier allowances, scheduling limits, and pricing can change. Verify the current provider documentation before deployment.

**Important correction:** Render's free web service is available, but
Render Cron Jobs are not free. The documented minimum is \$1 per month
per cron service.

**Options to consider**

-   **GitHub Actions:** Easiest if the code is already in GitHub.
-   **Google Cloud Scheduler:** Good if the backend is on Google Cloud
    Run.
-   **Vercel Cron:** Convenient if the backend is on Vercel.
-   **Cloudflare Cron:** Good if the backend is on Cloudflare Workers.

The manual sync button can trigger the same synchronization endpoint
regardless of which scheduler is selected.

------------------------------------------------------------------------

## 5. Authentication Platforms

If the project has a public portfolio plus a private administrator
dashboard, authentication is needed.

  Platform                  Free possibility        Use
  ------------------------- ----------------------- ----------------------------------
  Supabase Auth             Included in free plan   User authentication
  Firebase Authentication   Free allowances         User login
  Clerk                     Free plan               Authentication UI and management
  Auth0                     Free tier               Authentication
  Better Auth               Open-source             Self-managed authentication

Supabase Auth is convenient if Supabase is also the selected database.

Possible access model:

-   **Public visitors:** View published projects.
-   **Administrator:** Create, edit, delete, and synchronize projects.
-   **Notion:** Remains the source of truth for project information.

Never expose the Notion integration secret or database write credentials
to the browser.

------------------------------------------------------------------------

## 6. Complete Deployable Combinations

These are realistic architectures rather than isolated product
recommendations.

### Architecture A --- Conventional Python Stack

**Best for learning FastAPI**

  Layer                    Platform           Responsibility
  ------------------------ ------------------ ----------------------------
  Frontend                 Cloudflare Pages   React + Vite website
  Backend                  Render             FastAPI web service
  Database                 Neon               PostgreSQL
  Manual synchronization   HTTP endpoint      Website triggers sync
  Daily synchronization    GitHub Actions     Calls the backend endpoint

**Advantages**

-   Normal Python development.
-   Simple separation of responsibilities.
-   PostgreSQL database.
-   Free static hosting.
-   Good learning experience.

**Disadvantages**

-   Render cold starts.
-   GitHub Actions is an additional service.
-   Free Render hosting is not guaranteed production uptime.

### Architecture B --- Google Cloud Stack

**Best serverless Python option**

  Layer                    Platform           Responsibility
  ------------------------ ------------------ -----------------------------------
  Frontend                 Cloudflare Pages   React website
  Backend                  Google Cloud Run   Containerized FastAPI application
  Database                 Neon or Supabase   PostgreSQL
  Manual synchronization   HTTP endpoint      Website triggers sync
  Daily synchronization    Cloud Scheduler    Calls the backend endpoint

**Advantages**

-   Proper containerized Python backend.
-   Scales down when idle.
-   Daily scheduling.
-   No need for GitHub Actions.

**Disadvantages**

-   More complex setup.
-   Billing configuration required.
-   Google Cloud resources need monitoring.

### Architecture C --- All-in-One Cloudflare Ecosystem

**Best lightweight infrastructure**

  -----------------------------------------------------------------------
  Layer                   Platform                Responsibility
  ----------------------- ----------------------- -----------------------
  Frontend                Cloudflare Pages        Website

  Backend                 Cloudflare Workers      JavaScript/TypeScript
                                                  backend or Python
                                                  Workers

  Database                Cloudflare D1           SQLite-compatible
                                                  database

  Daily synchronization   Cron Triggers           Runs scheduled
                                                  synchronization
  -----------------------------------------------------------------------

**Advantages**

-   Generous free limits.
-   No traditional server to maintain.
-   Static hosting, API, database, and scheduler in one ecosystem.

**Disadvantages**

-   Not conventional FastAPI development.
-   Different database technology.
-   More JavaScript/TypeScript-oriented architecture.

### Architecture D --- Vercel Ecosystem

**Best frontend/backend convenience**

  -----------------------------------------------------------------------
  Layer                   Platform                Responsibility
  ----------------------- ----------------------- -----------------------
  Frontend and backend    Vercel                  React + Vite /
                                                  Next.js + Python
                                                  functions

  Database                Neon or Supabase        PostgreSQL

  Daily synchronization   Vercel Cron             Triggers
                                                  synchronization
  -----------------------------------------------------------------------

**Advantages**

-   Frontend and backend can live in one repository.
-   Daily cron support.
-   Easy GitHub deployment.

**Disadvantages**

-   Serverless execution limits.
-   Hobby plan usage restrictions.
-   Less like managing a traditional FastAPI server.

------------------------------------------------------------------------

## 7. Overall Comparison

This is a suitability assessment for the project, not a universal
performance ranking.

  ----------------------------------------------------------------------------
  Platform         Python         Daily          Persistent DB  ₱0 potential
                                  automation     option         
  ---------------- -------------- -------------- -------------- --------------
  Render           Excellent      External       External DB    Yes
                                  scheduler                     

  Google Cloud Run Excellent      Cloud          External DB    Yes\*
                                  Scheduler                     

  Vercel           Good           Built-in Cron  External DB    Yes\*

  AWS Lambda       Excellent      EventBridge    External DB    Yes\*

  Azure Functions  Excellent      Timer Trigger  External DB    Yes\*

  Koyeb            Excellent      External       External DB    Yes
                                  scheduler                     

  Cloudflare       Different      Built-in Cron  D1             Yes
  Workers          runtime                                      

  PythonAnywhere   Good           Paid feature   Limited        Restricted
  ----------------------------------------------------------------------------

\* Free within quotas and subject to account, billing, and usage
conditions. Render and Koyeb also have resource restrictions.

------------------------------------------------------------------------

## 8. Final Shortlist

For this project, these are the five combinations worth evaluating most
closely.

### 1. Cloud Run + FastAPI + Neon

**Best overall**

-   Proper Python backend.
-   Serverless deployment.
-   Daily scheduler.
-   PostgreSQL.
-   Good backend engineering experience.

### 2. Render + FastAPI + Neon + GitHub Actions

-   Easiest conventional Python deployment.
-   Free web service.
-   Daily automation through GitHub.
-   Database independent of hosting.

### 3. Vercel + FastAPI + Supabase

-   Convenient frontend and backend deployment.
-   Built-in daily scheduling.
-   Authentication and PostgreSQL available.

### 4. Cloudflare Workers + D1

-   Lightweight infrastructure.
-   Generous free request limits.
-   No traditional Python server.

### 5. Oracle Cloud + FastAPI + PostgreSQL

-   Traditional server architecture.
-   Full control.
-   Always Free compute options.
-   More maintenance and configuration.

------------------------------------------------------------------------

## 9. Recommended Architecture

**Cloud Run + FastAPI + Neon + Cloudflare Pages**

  Component    Selection
  ------------ ------------------------
  Backend      Google Cloud Run
  Database     Neon PostgreSQL
  Frontend     Cloudflare Pages
  Automation   Google Cloud Scheduler

### Data flow

``` text
Notion
   |
   v
FastAPI (Google Cloud Run)
   |
   v
Neon PostgreSQL
   |
   v
React website (Cloudflare Pages)
```

### Synchronization flow

``` text
Manual:
Website -> FastAPI -> Notion -> Neon

Daily:
Cloud Scheduler -> FastAPI -> Notion -> Neon

Website reads:
React website -> FastAPI -> Neon
```

All components have free usage possibilities. Google Cloud requires
billing configuration, so monitor usage and configure budget alerts. A
zero-cost outcome is possible within the allowances, but it is not
guaranteed under every circumstance.

------------------------------------------------------------------------

## 10. Avoid Overengineering

For a project portfolio containing perhaps 10--100 projects, you do not
need:

-   Kubernetes.
-   Redis.
-   Multiple databases.
-   Microservices.
-   A continuously running background worker.
-   An expensive cloud server.

A single FastAPI application with a PostgreSQL database is sufficient.

Keep the architecture modular so you can replace Render with Cloud Run,
Neon with Supabase, or Cloudflare Pages with Vercel without rewriting
the entire application.

### References for Further Comparison

-   [Render free tier](https://render.com/docs/free)
-   [Google Cloud Run pricing](https://cloud.google.com/run/pricing)
-   [Vercel pricing](https://vercel.com/pricing)
-   [Neon pricing](https://neon.com/pricing)
-   [Supabase pricing](https://supabase.com/pricing)
-   [Cloudflare Workers
    limits](https://developers.cloudflare.com/workers/platform/limits/)
-   [AWS Lambda pricing](https://aws.amazon.com/lambda/pricing/)

**Main takeaway:** Choose your backend hosting based on the Python
execution model you want to learn, not simply which company has the
biggest free quota.

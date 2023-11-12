---
layout: post
title:  "Development Stages of Analytics Practice"
tags: management
---


**

Development Stages of Analytical Databases

Organizations have datasets scattered around in various departments. They want to be able to gain analytical insights from combining one or more of these datasets into something that can provide additional value. 

# Proof of concept

While the value of analytics is commonly understood to be positive, it comes with development and maintenance costs, which need to be justified. This is best done with a low-cost proof of concept (i.e. POC), where a small team identifies the lowest hanging analytical fruit in the organization and attempts to show the value of analytics. 

  

Deliverables

- Identify key teams and data sources that are needed to provide input to the analytical database. 
    
- A convincing proof of concept that justifies maintenance and further development of the analytical database and the products. 
    

Costs

- Human requirements
    

- We need all rounders with good intuition (not necessarily expert) of data, systems and business sense. This person should have enough understanding to hack existing components together to get something working without necessarily knowing about the details. The most essential skill is being able to understand the data and the business value. 
    
- Demonstrating business value of the POC tends to depend heavily on communication and corporate appetite. Legality of the potential product and stakeholder buy-in should also be reviewed at this point so managerial support is also essential at this stage.
    
- If the cumulative size of the input datasets is expected to reach beyond the computational limits of a single computer (e.g. raw dataset size of about 8GB for a computer with 16GB of memory), we may need the part time support of a data engineer, whose primary role is to ingest the input datasets so that queries can be run on these datasets.
    

- Technical costs
    

- There is no engineering or scaling effort at this point other than what is necessary to demonstrate business value. Logic that is built at this stage is focused on the end-goal and not maintainability. 
    
- Computational resources may be provisioned on an ad hoc basis for a limited time period (i.e. physical computers or a cloud instance) during the POC.
    

- Monthly cloud costs for databases are usually separated into storage (size of the database), compute (how much time and resources it takes to run queries) and bandwidth (how much data is transferred into and out of the server). Some cloud services may offer a free tier. 
    

- Data access
    

- Permissions and confidentiality agreements may be granted on an individual basis. 
    
- Data may be stored in locations which are only accessible by specific individuals (i.e. physical computers, private cloud instances). IT support and security review may be required. There may also be regional requirements for data storage (i.e. requiring that the data may not leave the host country). 
    
- Terms and conditions of data storage should also be agreed upon in the event that data is allowed to leave the control of the teams responsible for creating and holding the data.
    

# Delivering and Maintenance

Once the organization sees that business value is worth some investigation into the investment required, we may productize the proof-of-concept. A product differs from a proof-of-concept in the sense that during the former, we only need to show that it can succeed, but for the latter, we need to make sure that it cannot fail and we have contingency plans in the event that it does fail. This also means that we need to manage transitions of human capital in the organization, since the team or team composition responsible for this product may change over time. 

  

Deliverables

- Identify service standards and ingestion methods of input data sources.
    
- Identify required services standards and downstream users of the analytical database and the products.
    
- Monitoring and remediation strategy in case of failure. 
    

Costs

- Human requirements
    

- We need narrow experts in databases and software engineers.
    

- SQL and database experts for relational databases.
    
- Software engineers are needed to manage ingestion and storage of unstructured data (e.g. images, scans, sound) and accessing these data. 
    
- Software engineers are also needed to maintain pipelines that transform data sources to datasets that power the product. 
    

- Technical management roles may be required to coordinate efforts and report to stakeholders.
    
- Depending on service standards, we may need personnel to be available to resolve faults outside of normal working hours.
    
- If physical computational resources are required, we need support from IT teams. If cloud resources are required, we need support from cloud platform teams.
    

- Technical costs 
    

- Ongoing and future computational resources need to be provisioned. If physical computers are being used, one needs to factor in depreciation of assets and downtime. If cloud resources are used, we need cost monitoring and estimates. 
    

- Data access 
    

- Team or role-based access to the production systems and data. Individual access is still okay, but they must only be granted permissions or access due to the fact that they are in a relevant team or are performing a relevant role. We may need ongoing security or legal team support for data access to manage access control and security auditing.
    
- Similar access management and review for downstream users may also need to be supported. 
    

# Extending the Analytical Platform

Platform building should be a part of the process of continuing to deliver value to the organization. 

  

Deliverables

- Reorganizing reusable components of the analytical system to integrate more data sources.
    
- Support data exploration for new potential analytical applications. 
    
- Pipeline integration that automates dependent jobs transforming input data sources to downstream products or other datasets. 
    

  

The nature of costs are similar to the previous section, albeit at a larger scale. The saying that “Quantity has a Quality” of its own definitely applies here and the path forward varies significantly by organization and their history. It’s also not necessarily true that every organization wants to develop an analytical platform due to cost reasons.

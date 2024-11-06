
# RESTful Infrastructure Documentation

## Section 1: Information

This documentation provides an overview of the RESTful Infrastructure application, its components, setup, and usage instructions.

The RESTful Infrastructure application consists of multiple components, each designed to handle specific aspects of the system. Below is a detailed breakdown of each component and how to interact with them.

## Documentation Links

Documentation to specific components of the RESTful infrastructure can be found using the following links provided:

- **[Server Documentation](https://github.com/ibadrather/RESTful_Infrastructure/blob/documentation/server/server/README.md)**

  Provides detailed information on setting up and managing the server for the project.

- **[Database Documentation](https://github.com/ibadrather/RESTful_Infrastructure/blob/documentation/server/server/database/README.md)**

  Contains specifications and configuration details for the database.

- **[Vehicle Client Documentation](https://github.com/ibadrather/RESTful_Infrastructure/blob/documentation/server/vehicle_client/README.md)**

  Describes the client-side code and how to interact with the vehicle management API.

## System Requirements

- **Operating System** : This application is built and tested exclusively on **Linux Ubuntu** . Using it on other operating systems may lead to unexpected behavior.

- **Hosting** : The application components are hosted on free-tier instances, which may enter sleep mode after periods of inactivity. If you experience a delay, please allow a few minutes for the services to restart. Your patience is appreciated.

## Components

### A. API

The API serves as the backend for the application, handling requests and providing data to the client.

- **Documentation** : The API is documented using Swagger UI, which provides an interactive interface to explore and test the API endpoints.
  - **Swagger UI** : [Access API Documentation here](https://restful-infrastructure.onrender.com/docs)

- **Hosting** : The API is hosted on a free instance through Render.com. Due to this, the API may go into sleep mode during inactivity and could take a few minutes to resume.

- **Further Details** : For more information on setting up or customizing the API, refer to the `server/README.md` file.

### B. Client

The client is a vehicle-specific module that interacts with the API to manage and retrieve data related to vehicle operations.

- **Directory** : The client code is located in the `vehicle_client/` directory.

- **Instructions** : Detailed instructions for running the client are available in `vehicle_client/README.md`.

### C. API WebApp (Optional)
A simple frontend is available as a proof of concept, built using **Streamlit** . This web app demonstrates how data can be visualized but is not a full-featured production version.
- **WebApp** : [Access the WebApp here](https://vehicle-rest-api.streamlit.app/)

> **Note** : The WebApp is designed primarily as a demonstration and may not include the same refinements and features as the core API and client components.

---

## Section 2: Programming Task – REST API - Server and Client

### Task Concept
Develop a (very) small “RESTful infrastructure” by setting up a database (DB), implementing a REST API server as well as a REST API client. The client shall be able to store data through the API as well as retrieve this data. There is no specification of how this data should look like. You are also free in the choice of frameworks and database management systems.

### Boundary Conditions
1. The REST API server shall be written in Python.
2. The REST API client shall be written in C++.
3. The client shall save data persistently within the database through the REST API.
4. The client shall read data from the database through the REST API.
5. The client shall print information about this data exchange to the console.
6. Use a build system (for C++); e.g., make, cmake, ninja, etc.
7. You are free in the choice of frameworks, DBMS, operating system, deployment.

### Concept Image

![Basic Infrastructure Diagram](RESTful_infracstructure_basic_architecture.png)

### Task Implementation Specification
Implement a REST infrastructure consisting of:
- **Database**
- **REST API Server** (written in Python)
- **REST API Client** (written in C++)
- **Working example with meaningful output to the console**

Implement at least 3 API endpoints that:
- Store data (coming from the client)
- Read data (coming from the database)
- Update data that is already present in the database

---

## Section 3: Future Tasks and Improvements

- **Upgrade Database to PostgreSQL** : For production-scale use, PostgreSQL is more robust than SQLite, supporting multi-client access and large datasets.

- **Enhanced Testing for CI/CD** : Add more tests to ensure stability and reliability in deployment pipelines.

- **Asynchronous API** : Convert API calls to async for improved performance under heavy load.

- **Robust Error Handling** : Implement more detailed error management to improve reliability and troubleshooting.

- **API Security** : Add TLS for secure client-server verification.

- **Verbose Logging** : Implement comprehensive logging for better monitoring and debugging.

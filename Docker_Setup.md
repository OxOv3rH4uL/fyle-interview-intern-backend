# Fyle Assignment Docker Setup

## **Note:** Make sure you have Docker installed and running.

## **Steps:**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/OxOv3rH4uL/fyle-interview-intern-backend
   ```

2. **We can build in 2 ways**
  - *Using Docker Compose*
  ```bash
  docker-compose up -d
  ```

  - *Using Dockerfile*
  ```bash
  docker build -t fyle-backend .
  docker run -p 7755:7755 fyle-backend
  ```
3: **Enjoy the Service:**
  ```bash
  http://127.0.0.1:7755/
  ```


## **Conclusion:**
This is how we can deploy the RESTAPI Service using Docker. All the listed APIs have been created. Tests coverage is around 96%.

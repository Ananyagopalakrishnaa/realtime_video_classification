Installing Docker Desktop on Windows
Installation Steps:

1. Download Docker Desktop:
   - Visit https://www.docker.com/products/docker-desktop
   - Download the Docker Desktop installer and run it.

2. Install Docker Desktop:
   - Follow the on-screen instructions to install Docker Desktop.
   - You might be prompted to enable the WSL 2 backend during the installation. Allow it, as it provides better performance and compatibility.

3. Start Docker Desktop:
   - Once installed, start Docker Desktop. You should see the Docker icon in your system tray when Docker is running.
------------------------------------------------------------------------------------------------------------------------------------------
Installing Docker Desktop on macOS
Installation Steps:

Download Docker Desktop:

Visit https://www.docker.com/products/docker-desktop
Download the Docker Desktop installer for macOS and open it.
Install Docker Desktop:

Follow the on-screen instructions to install Docker Desktop.
When prompted, drag and drop Docker.app to your Applications folder.
Start Docker Desktop:

Open Docker from your Applications folder.
You should see the Docker icon in your menu bar when Docker is running.
------------------------------------------------------------------------------------------------------------------------------------------
Running Docker Project:

1. Navigate to Project Directory:
   - Open a terminal or command prompt and navigate to the directory where the folder is located.
    cd /path to the folder

2. Setting up the youtube API: create a .env file and provide your API key here.
   YOUTUBE_API_KEY=your_api_key_here


3. Build and Run Docker Containers as a daemon process:
   docker-compose up -d --build 

4. To check the working of the containers:
    docker ps
    docker images

5. to check functionality of any 1 container:
    docker-compose logs <container_name>

6. to check the predictions made for the videos:
    docker-compose logs mlp_model

------------------------------------------------------------------------------------------------------------------------------------------

To stop the container
docker-compose down
---------------------------------------------------------------------------------------------------------

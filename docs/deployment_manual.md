# Police Forensics AI: Deployment Manual

This manual provides instructions for installing and running the Police Forensics AI "Cyber Command Terminal" on fresh laptops and servers in police precincts.

---

## Option 1: Standalone Windows Application (Recommended for Laptops)

We have packaged the entire application (including the PyTorch neural network, RealESRGAN/CodeFormer restoration models, and the Gradio UI) into a standalone Windows folder. This is the easiest way to run the software on a precinct computer without installing Python or compiling code.

### System Requirements
* **OS:** Windows 10 or Windows 11 (64-bit)
* **RAM:** 16 GB minimum (32 GB recommended for heavy image restoration)
* **Disk Space:** 5 GB free space

### Installation Steps (Detailed)

**Step 1: Copy the Application from this PC**
1. On the build machine, go to the project folder (`PoliceForensicsAI`) and open the **`dist`** folder.
2. Inside `dist`, you will see a folder named **`CyberTerminal`**.
3. Right-click that `CyberTerminal` folder and copy it onto a USB thumb drive.

**Step 2: Paste it on the New Laptop**
1. Plug the USB drive into the new laptop.
2. Drag and drop the `CyberTerminal` folder anywhere you want (for example, directly onto the Desktop).

**Step 3: Add your Secret Key**
1. Open the `CyberTerminal` folder on the new laptop.
2. Right-click in the empty white space inside the folder, select **New**, and click **Text Document**.
3. Name this new file exactly **`.env`** (make sure you delete the `.txt` part).
4. Open the `.env` file in Notepad, paste in your API key like this:
   `GEMINI_API_KEY=your_actual_key_here`
5. Save and close Notepad.

**Step 4: Run It!**
1. Still inside that folder, double-click **`CyberTerminal.exe`**.
2. A black terminal window will pop up (don't close it!). 
3. Open Google Chrome or Microsoft Edge and type **`http://127.0.0.1:7860`** in the address bar.
4. The full Cyber Command Terminal will appear on the new laptop, ready to process evidence!

---

## Option 2: Docker Container (Recommended for Precinct Servers)

If you are deploying the application to a central precinct server or a cloud instance, use the Docker container. This ensures identical execution regardless of the host OS (Linux, Windows, or macOS).

### Prerequisites
* Docker installed on the host machine.
* A `.env` file containing your `GEMINI_API_KEY`.

### Installation Steps

1. **Build the Docker Image**
   Navigate to the root directory of the project (where the `Dockerfile` is located) and run:
   ```bash
   docker build -t police-forensics-ai .
   ```

2. **Run the Container**
   Start the container, passing in your `.env` file and mapping port 7860 to the host:
   ```bash
   docker run -p 7860:7860 --env-file .env police-forensics-ai
   ```

3. **Access the Application**
   Open any web browser on the network and navigate to the server's IP address on port 7860 (e.g., `http://localhost:7860` or `http://192.168.1.100:7860`).

---

## Option 3: Mobile Access (Smartphones / Field Use)

You **cannot** install the standalone application or the Docker container directly onto an Android or iOS smartphone. The neural network algorithms require dedicated Desktop-class RAM and GPUs. 

However, officers can easily access the system from their phones in the field:
1. Ensure the application is running on your central Windows or Linux machine (using Option 1 or Option 2).
2. On the officer's smartphone, open Google Chrome or Safari. (Make sure the phone is connected to the same Wi-Fi network as the laptop!)
3. In the address bar, type the exact IP address of the laptop followed by port 7860. Based on your current network, use one of the following:
   * **`http://172.22.9.226:7860`** (Primary Network)
   * **`http://192.168.137.1:7860`** (Secondary/Hotspot Network)
4. **Note on Security:** Your browser may say "Not Secure." This is perfectly normal for local HTTP traffic. Because the data is travelling directly from your phone to your laptop over your private Wi-Fi router, it never touches the public internet and cannot be intercepted from the outside. You can safely ignore the warning.
5. The full Cyber Terminal interface will load on the phone. Officers can upload evidence photos directly from their camera roll, and the heavy processing will be offloaded to the precinct server.

---

## Option 4: Air-Gapped Offline Mode (Ollama Integration)

If your precinct server or laptop has a dedicated NVIDIA GPU and 16GB+ of RAM, you can run the entire extraction process 100% offline using **Llama 3.2 Vision**. This is the highest level of security and does not require an internet connection or API key.

### Installation Steps
1. Navigate to [https://ollama.ai/](https://ollama.ai/) and download the Windows installer.
2. Install Ollama and open a Command Prompt (Terminal).
3. Type the following command to download the 11-Billion parameter Llama vision model:
   ```cmd
   ollama run llama3.2-vision
   ```
4. Wait for the download to complete (it is an 8GB file, so it may take time). Once downloaded, Ollama will run quietly in the background on port `11434`.
5. Open the Cyber Command Terminal UI and simply select **Llama 3.2 Vision** under the LLM Provider radio buttons. 

The system will now route all forensic extraction entirely through your local GPU, ensuring the image data never leaves the physical room!

---

## Troubleshooting

* **"API Key Not Found" Error:** Ensure the `.env` file is in the exact same folder as the `.exe` (for standalone) or passed correctly via `--env-file` (for Docker). Make sure Windows didn't hide the extension and name it `.env.txt`.
* **Out of Memory Crash:** Processing large 4K images with RealESRGAN can consume significant RAM. If the application crashes during the "AI Restoration" phase, try reducing the image resolution before uploading, or disable the Deep Learning toggle.

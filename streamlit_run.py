import subprocess
import base64
import pandas as pd
import time

# Create an empty list to store the test results
test_results = []
website_name = input("Enter website address or IP Address: ")
# Iterate over the lines, skipping the header
if website_name != "":
  output_fil = website_name + ".csv"
  print("Started Scanning " + website_name)
  save_excel = subprocess.run(
      ["dnsrecon", "-d", website_name, "-c", output_fil],
      check=True,
      capture_output=True,
      text=True)
  time.sleep(10)
  print("Scanned Results Saved in CSV file")
  df = pd.read_csv(str(website_name + ".csv"))
  print(df)
  # Define the input and output file paths
  input_file = output_fil
  output_file = website_name + ".txt"
  # Open the input file for reading
  with open(input_file, "r") as file:
    # Read the lines from the file
    lines = file.readlines()
  for line in lines[1:]:
    # Split the line into fields
    fields = line.strip().split(",")

    # Get the IP address and target from the fields
    ip_address = fields[2]
    target = fields[3]

    print(f"Testing started for {ip_address} ({target})")

    # Perform the tests
    ping_result = subprocess.run(["ping", "-c", "1", ip_address],capture_output=True,text=True)
    nslookup_result = subprocess.run(["nslookup", ip_address],capture_output=True,text=True)
    nmap_result = subprocess.run(["nmap", ip_address],capture_output=True,text=True)
    whois_result = subprocess.run(["whois", ip_address],capture_output=True,text=True)

    print(f"Testing finished for {ip_address} ({target})")

    # Store the test results
    test_result = f"--- Test results for {ip_address} ({target}) ---\n"
    test_result += "\nPing Result:\n" + ping_result.stdout + "\n"
    test_result += "\nNSLookup Result:\n" + nslookup_result.stdout + "\n"
    test_result += "\nNmap Result:\n" + nmap_result.stdout + "\n"
    test_result += "\nWhois Result:\n" + whois_result.stdout + "\n"

    # Add the test result to the list
    test_results.append(test_result)
    # Write each test result to the file
    with open(f"{website_name}.txt", "w") as out_file:
        for result in test_results:
            out_file.write(result + "\n")  # Add a line break after each result


  # Save the test results to the output file

  import subprocess
  import pandas as pd

  # Prompt for server IP address
  server_ip = website_name

  # Specify the ports to scan
  vulnerable_ports = "20,21,22,23,25,53,67,68,69,80,110,119,123,137,138,139,143,161,162,389,443,445,465,514,636,993,995,1433,1521,3306"

  # Build the Nmap command
  command = f"nmap -Pn -p {vulnerable_ports} {server_ip}"

  # Execute the Nmap command and capture the output
  try:
    output = subprocess.check_output(command,
                                     shell=True,
                                     stderr=subprocess.STDOUT)
    output_str = output.decode()
    print(output_str)
  except subprocess.CalledProcessError as e:
    print(f"An error occurred while executing the Nmap command: {e}")
    exit()

// Extract all text content from the webpage
let pageText = document.body.innerText;

// Regular expression to find all IP addresses
let ipRegex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/g;
let ips = pageText.match(ipRegex) || []; // Get all matches or return an empty array if no IPs are found

// Remove duplicate IPs
ips = [...new Set(ips)];

// Check if any IPs were found
if (ips.length === 0) {
    console.error("❌ No IP addresses found on this page!");
} else {
    // Convert the IP list to a text file
    let blob = new Blob([ips.join("\n")], { type: "text/plain" });

    // Create a download link
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ips.txt"; // Filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    console.log("✅ File 'ips.txt' has been downloaded successfully! It contains " + ips.length + " IP addresses.");
}

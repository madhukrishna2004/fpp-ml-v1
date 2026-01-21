async function loadLogs() {
  const res = await fetch("/admin/logs");
  const data = await res.json();
  document.getElementById("logs").innerText =
    JSON.stringify(data, null, 2);
}
loadLogs();

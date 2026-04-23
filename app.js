let data = {};

document.getElementById("upload").addEventListener("change", handleFile);

function handleFile(e) {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.onload = function (evt) {
    const workbook = XLSX.read(evt.target.result, { type: "binary" });

    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    const json = XLSX.utils.sheet_to_json(sheet);

    // 👇 Map your Excel columns here
    data = {
      leads: json[0]["Leads"] || 0,
      spend: json[0]["Spend"] || 0,
      visits: json[0]["Visits"] || 0,
      bookings: json[0]["Bookings"] || 0,
      targetVisits: json[0]["Target Visits"] || 0
    };

    calculateMetrics();
    showPreview();
  };

  reader.readAsBinaryString(file);
}

function calculateMetrics() {
  data.cpl = (data.spend / data.leads).toFixed(2);
  data.achievement = (
    (data.visits / data.targetVisits) * 100
  ).toFixed(1);
}

function showPreview() {
  document.getElementById("preview").innerHTML = `
    <p>Leads: ${data.leads}</p>
    <p>Spend: ₹${data.spend}</p>
    <p>CPL: ₹${data.cpl}</p>
    <p>Visits: ${data.visits}</p>
    <p>Achievement: ${data.achievement}%</p>
    <p>Bookings: ${data.bookings}</p>
  `;
}

function generatePPT() {
  let pptx = new PptxGenJS();

  // Slide 1
  let slide1 = pptx.addSlide();
  slide1.addText("Weekly Report", { x:1, y:1, fontSize:24 });

  // Slide 2
  let slide2 = pptx.addSlide();
  slide2.addText(`Leads: ${data.leads}`, { x:1, y:1 });
  slide2.addText(`Spend: ₹${data.spend}`, { x:1, y:1.5 });
  slide2.addText(`CPL: ₹${data.cpl}`, { x:1, y:2 });

  // Slide 3
  let slide3 = pptx.addSlide();
  slide3.addText(`Visits: ${data.visits}`, { x:1, y:1 });
  slide3.addText(`Achievement: ${data.achievement}%`, { x:1, y:1.5 });
  slide3.addText(`Bookings: ${data.bookings}`, { x:1, y:2 });

  pptx.writeFile("Weekly_Report.pptx");
}

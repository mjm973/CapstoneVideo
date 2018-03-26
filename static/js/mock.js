let checkId = null;

let checkFile = () => {
  console.log("querying filesystem...");
  fetch('http://localhost:5050/check/', {
    body: JSON.stringify({}),
    method: 'POST',
    mode: 'no-cors'
  }).then((res) => {
    return res.json();
  }).then((wat) => {
    console.log(wat);
    if (wat[0]) {
      console.log("found it!");
      //clearInterval(checkId);
      return;
    }
    setTimeout(checkFile, 1500);
  });
}

document.addEventListener('DOMContentLoaded', ()=> {
  console.log("loaded!");
  //checkId = setInterval(checkFile, 1000);
  //console.log("checkId is", checkId);
  checkFile();
});

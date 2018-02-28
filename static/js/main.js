document.addEventListener('DOMContentLoaded', ()=> {
  console.log("loaded!");
  setInterval(checkFile, 1000);
});

let checkFile = () => {
  fetch('fs').then((res) => {
    return res.json();
  }).then((wat) => {
    console.log(wat);
  });
}

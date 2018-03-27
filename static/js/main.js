let setPassBehavior = () => {
  let form = document.getElementById('pass-form');
  let passR = document.getElementById('pass-r');
  let passG = document.getElementById('pass-g');
  let passB = document.getElementById('pass-b');
  passR.addEventListener('keydown', (e) => {
    if (e.keyCode == 8) { // backspace

    } else {
      setTimeout(() => {passG.focus();}, 10);
    }
  });
  passG.addEventListener('keydown', (e) => {
    if (e.keyCode == 8) { // backspace
      setTimeout(() => {passR.focus();}, 10);
    } else {
      setTimeout(() => {passB.focus();}, 10);
    }
  });
  passB.addEventListener('keydown', (e) => {
    if (e.keyCode == 8) { // backspace
      setTimeout(() => {passG.focus();}, 10);
    } else if (e.keyCode == 13) { // return
      form.submit();
    } else {
      if (passB.value) {
        e.preventDefault();
      }
    }
  });
}

let setLockBehavior = () => {
  let retry = document.getElementsByClassName("lock");
  if (retry.length > 0) {
    document.addEventListener('keydown', (e) => {
      e.preventDefault();
      if (e.keyCode == 13) { // return
        window.location.reload(true);
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  console.log("loaded!");

  setPassBehavior();
  setLockBehavior();
});

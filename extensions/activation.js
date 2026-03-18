const extension1 = JSON.parse(localStorage.getItem("extension1"));
const extension2 = JSON.parse(localStorage.getItem("extension2"));
const extension3 = JSON.parse(localStorage.getItem("extension3"));
const extensionLimitError = document.createElement("div");
extensionLimitError.style.position = "fixed";
extensionLimitError.style.bottom = "0px";
extensionLimitError.style.width = "100%";
extensionLimitError.style.height = "16%";
extensionLimitError.style.zIndex = 999;
extensionLimitError.innerHTML = "Exceeded extension limit";
extensionLimitError.style.fontWeight = "bold";
extensionLimitError.style.fontFamily = "Courier New";
if (localStorage.getItem("extension4") === null) {} else {
  document.body.appendChild(extensionLimitError);
  setTimeout(function() {
    extensionLimitError.remove();
  }, 3000);
}
if (extension1 === null) {} else {
  eval(extension1.script);
}
if (extension2 === null) {} else {
  eval(extension2.script);
}
if (extension3 === null) {} else {
  eval(extension3.script);
}

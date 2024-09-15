function toggleOverlay() {
  modal.style.display = "block";
}
function closePopup() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
function tutorial() {
  var tour = new Tour({
    steps: [
    {
      element: "#navbarBasicExample",
      title: "Title of my step",
      content: "Content of my step"
    },
    {
      element: "#welcome",
      title: "Name",
      content: "Content of my step"
    }
  ]});
  tour.init();
  tour.start();
}
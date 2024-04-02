const form = document.getElementById("add-criteria-form");
const distElem = document.getElementById("search_distance");
const unitsElem = document.getElementById("dist-units");

document.querySelectorAll("input.submit-input").forEach((elem) => {
  elem.addEventListener("click", function (e) {
    e.preventDefault();

    if (unitsElem.value === "km") {
      distElem.value = +distElem.value * 0.621371;
    }

    const formaction = elem.dataset.formaction;
    form.action = formaction;
    form.submit();
  });
});

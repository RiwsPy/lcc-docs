// reset des filtres et selects
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#search-text").value = ""
  document.querySelector("#translation-all").checked = true
  document.querySelector("#quality-all").checked = true
  document.querySelector("#game-all").checked = true
  document.querySelector("#category-all").checked = true
  updateCategoryCount()
})

function updateCategoryCount() {
  // ajout du count
  let containerCategories = document.querySelectorAll(".table .category_container")
  containerCategories.forEach(category => {
    let catMods = category.querySelectorAll(".row.mod:not(.hidden)")
    category.querySelector(".category_name").setAttribute("data-count", catMods.length)
  })
}

function filterMod() {
  const mods = Array.from(document.querySelectorAll(".table .row.mod"))
  let modByName = filterByName(mods)
  let modByGame = filterByGame(mods)
  let modByTranslation = filterByTranslation(mods)
  let modByQuality = filterByQuality(mods)
  let modsFiltered = mods

  if (modByName !== null) {
    modsFiltered = modByName
  }
  if (modByGame !== null) {
    modsFiltered = modByGame.filter(elt => new Set(modsFiltered).has(elt))
  }
  if (modByTranslation !== null) {
    modsFiltered = modByTranslation.filter(elt => new Set(modsFiltered).has(elt))
  }
  if (modByQuality !== null) {
    modsFiltered = modByQuality.filter(elt => new Set(modsFiltered).has(elt))
  }

  mods.forEach(mod => mod.classList.add("hidden"))
  modsFiltered.forEach(mod => mod.classList.remove("hidden"))

  // check des catégories (les enlèvent si aucun résultat n'est trouvé)
  let categories = document.querySelectorAll(".table .category_container .category")
  categories.forEach(category => category.style.display = category.querySelector(".row.mod:not(.hidden)") ? "" : "none")

  updateCategoryCount()
}

function filterByGame(mods) {
  const checkedGame = document.querySelector(".search_item.game input[type='radio']:checked")
  let modsFiltered = null
  if (checkedGame.value !== "") {
    modsFiltered = Array()
    mods.forEach(mod => {
      for (let modGame of mod.querySelectorAll(".jeu *")) {
        if (checkedGame.value == modGame.textContent) {
          modsFiltered.push(mod)
          break
        }
      }
    })
  }
  return modsFiltered
}

function filterByName(mods) {
  const input = document.querySelector("#search-text")
  let modsFiltered = null
  if (input.value !== "") {
    let inputValue = input.value.toLowerCase()
    modsFiltered = Array.from(mods).filter(mod => mod.querySelector(".name").textContent.toLowerCase().includes(inputValue))
  }
  return modsFiltered
}

function filterByTranslation(mods) {
  const currentTranslation = document.querySelector("#translation-select input:checked").value
  if (currentTranslation == "") {
    return null
  }
  return Array.from(mods).filter(mod => mod.querySelector(".icons").textContent.includes(currentTranslation))
}

function filterByQuality(mods) {
  const currentQuality = document.querySelector("#quality-select input:checked").value
  if (currentQuality == "") {
    return null
  }
  return Array.from(mods).filter(mod => mod.querySelector(".icons").textContent.includes(currentQuality))
}

function filterByCategory() {
  const categoryChecked = document.querySelector(".search_item.category input[type='radio']:checked")
  const categories = Array.from(document.querySelectorAll(".category_container"))
  if (categoryChecked && categoryChecked.value !== "") {
    categories.forEach(category => {
      let categoryName = category.getAttribute("data-name")
      category.style.display = categoryChecked.value == categoryName ? "" : "none"
    })
  } else {
    categories.forEach(category => category.style.display = "")
  }
}
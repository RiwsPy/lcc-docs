// reset des filtres et selects
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#search-text").value = ""
  document.querySelector("#translation-all").checked = true
  document.querySelector("#quality-all").checked = true
  document.querySelector("#game-all").checked = true
  document.querySelector("#category-all").checked = true
  updateCategoryCount()
  toggleDetails()
})

window.addEventListener("resize", () => {
  toggleDetails()
});

function toggleDetails() {
  document.querySelectorAll("details.team").forEach(details => {
    if (window.innerWidth <= 900) {
      details.setAttribute("open", "");
    } else {
      details.removeAttribute("open");
    }
  })
}

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
  const categoryChecked = document.querySelector("#category-select input[type='radio']:checked")
  const categories = Array.from(document.querySelectorAll(".category_container"))
  if (categoryChecked && categoryChecked.value !== "") {
    categories.forEach(category => {
      let categoryName = category.getAttribute("data-name")
      category.parentElement.style.display = categoryChecked.value == categoryName ? "" : "none"
    })
  } else {
    categories.forEach(category => category.parentElement.style.display = "")
  }
}

// Avec la barre de recherche sticky, besoin de modifier la position d'affichage

document.addEventListener("DOMContentLoaded", function () {
  function adjustScroll(hash) {
    let target = document.querySelector(hash)
    if (target) {
      let offsetSearch = document.querySelector("#search_text").offsetHeight
      let offsetCategory = document.querySelector("summary.category_name").offsetHeight
      window.scrollTo({
        top: target.offsetTop - offsetSearch - offsetCategory - 1,
        behavior: "smooth"
      })
    }
  }

  // Ajustement au chargement de la page
  window.addEventListener("load", (event) => {
    if (window.location.hash) {
      adjustScroll(window.location.hash)
    }
  });

  // Ajustement au clic sur un lien avec une ancre
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function (event) {
      event.preventDefault()
      let hash = this.getAttribute("href")
      history.pushState(null, null, hash)
      adjustScroll(window.location.hash)
    })
  })

  // Changement de hash sans rechargement ou déplacement
  document.querySelectorAll('.update-hash-parent').forEach(balise => {
    balise.addEventListener("click", () => {
      let hash = balise.parentElement.id
      history.replaceState(null, null, window.location.href.split("#")[0] + `#${hash}`)
    })
  })
})
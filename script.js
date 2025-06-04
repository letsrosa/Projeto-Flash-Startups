const startups = [
  {
    nome: "Turbi",
    resumo: "Startup de aluguel de carros 100% digital que permite alugar um carro por algumas horas, dias ou meses, através de uma aplicação.",
    imagem: "img/turbi.png"
  },
  {
    nome: "Vammo",
    resumo: "Startup brasileira de mobilidade elétrica que oferece aluguel de motos elétricas para motoboys e entregadores de aplicativos.",
    imagem: "img/vammo.png"
  },
  {
    nome: "IGrenn",
    resumo: "Startup que se dedica a fornecer soluções de energia solar para redução de custos na conta de luz, sem exigir investimentos em instalação de placas solares.",
    imagem: "img/igreen.png"
  },
  { nome: "AquaSmart", resumo: "Sensores para economizar água urbana." },
  { nome: "JobLink", resumo: "Conecta jovens talentos com startups." },
  { nome: "TranspAI", resumo: "IA para otimizar rotas de transporte público." },
  { nome: "BioHackers", resumo: "Wearables de saúde personalizados." },
  { nome: "FoodTrace", resumo: "Blockchain para rastreio de alimentos." },
  { nome: "RescueBot", resumo: "Drones autônomos para resgates." }
];

let currentIndex = 0;
const cardsPerView = 3;
const cardContainer = document.getElementById("card-container");

function renderCards() {
  cardContainer.style.opacity = 0;
  setTimeout(() => {
    cardContainer.innerHTML = "";
    const slice = startups.slice(currentIndex, currentIndex + cardsPerView);
    slice.forEach((startup) => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        ${startup.imagem ? `<img src="${startup.imagem}" alt="${startup.nome}" class="card-img"/>` : ""}
        <strong>${startup.nome}</strong><br/>
        <small>${startup.resumo}</small>
      `;
      cardContainer.appendChild(div);
    });
    cardContainer.style.opacity = 1;
  }, 200);
}

function nextSlide() {
  if (currentIndex + cardsPerView < startups.length) {
    currentIndex += cardsPerView;
    renderCards();
  }
}

function prevSlide() {
  if (currentIndex - cardsPerView >= 0) {
    currentIndex -= cardsPerView;
    renderCards();
  }
}

document.addEventListener("DOMContentLoaded", renderCards);

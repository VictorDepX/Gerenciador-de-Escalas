// Define tema salvo no localStorage
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        document.documentElement.setAttribute("data-theme", savedTheme);
    }

    const monthInput = document.getElementById("mes_ano");
    if (monthInput) {
        monthInput.addEventListener("change", () => {
            const [ano, mes] = monthInput.value.split("-");
            const inputMes = document.getElementById("inputMes");
            const inputAno = document.getElementById("inputAno");
            if (inputMes && inputAno) {
                inputMes.value = mes;
                inputAno.value = ano;
            }
        });
    }
});

// Alterna entre tema claro e escuro
function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
}

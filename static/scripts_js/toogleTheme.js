// Функция для переключения темы
    function toggleTheme() {
        const body = document.body;
        body.classList.toggle("dark");
        body.classList.toggle("light");

        // Сохранение состояния в localStorage
        const isDarkMode = body.classList.contains("dark");
        localStorage.setItem("darkMode", isDarkMode);

        const themeSwitchContainer = document.getElementById('themeSwitchContainer');
        if (themeSwitchContainer) {
            const moonIcon = document.getElementById('moonIcon');
            const sunIcon = document.getElementById('sunIcon');

            // Применение соответствующего состояния иконок
            if (isDarkMode) {
                moonIcon.style.display = 'inline-block';
                sunIcon.style.display = 'none';
            } else {
                moonIcon.style.display = 'none';
                sunIcon.style.display = 'inline-block';
            }
        }
    }

    // Проверка состояния в localStorage при загрузке страницы
    document.addEventListener("DOMContentLoaded", function () {
        const isDarkMode = localStorage.getItem("darkMode") === "true";
        const body = document.body;
        const themeSwitch = document.getElementById("themeSwitch");
        const themeSwitchContainer = document.getElementById('themeSwitchContainer');
        const moonIcon = document.getElementById('moonIcon');
        const sunIcon = document.getElementById('sunIcon');

        // Установка состояния переключателя
        themeSwitch.checked = isDarkMode;

        // Применение соответствующего класса к телу страницы
        if (isDarkMode) {
            body.classList.add("dark");
            if (moonIcon && sunIcon) {
                moonIcon.style.display = 'inline-block';
                sunIcon.style.display = 'none';
            }
        } else {
            body.classList.remove("dark");
            if (moonIcon && sunIcon) {
                moonIcon.style.display = 'none';
                sunIcon.style.display = 'inline-block';
            }

        }
    });
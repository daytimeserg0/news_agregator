function searchPage() {
          // Получаем значение из поля ввода
          var searchText = $('#searchInput').val();

          const isDarkMode = document.body.classList.contains("dark");

          // Открываем новую страницу для отображения результатов поиска
          window.location.href = 'search-results?query=' + encodeURIComponent(searchText);

          // Предотвращаем отправку формы
          return false;
        }
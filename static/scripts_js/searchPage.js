function searchPage(event) {

          event.preventDefault();
          // Получаем значение из поля ввода
          var searchText = $('#searchInput').val();

          var container = document.getElementById('newsContainer'); // Замените 'yourContainerId' на ID вашего контейнера


          var formData = new FormData();
            formData.append('query', searchText);

            // Опции для fetch-запроса
            var options = {
                method: 'POST',
                body: formData,
            };

            // URL, к которому будет отправлен запрос
            var url = '/search';

            // Выполнение fetch-запроса
            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    // Обработка полученных данных
                    console.log(data);

                    // Пример обновления контейнера с новыми данными
                    container.innerHTML = ''; // Очищаем контейнер // Предположим, что у вас есть функция clearContainer для очистки контейнера
                    var searchData = data;

                    // Отображение результатов
                    var resultContainer = document.getElementById('newsContainer');

                    if (searchData.found_news % 100 >= 5 && searchData.found_news % 100 <= 20) {
                        resultContainer.innerHTML = `<h1 class="tags_finder">Найдено ${searchData.found_news} результатов по запросу "${searchData.or_search_query}"</h1>`;
                    } else if (searchData.found_news % 10 == 2 || searchData.found_news % 10 == 3 || searchData.found_news % 10 == 4) {
                        resultContainer.innerHTML = `<h1 class="tags_finder">Найдено ${searchData.found_news} результата по запросу "${searchData.or_search_query}"</h1>`;
                    } else if (searchData.found_news % 10 == 1) {
                        resultContainer.innerHTML = `<h1 class="tags_finder">Найден ${searchData.found_news} результат по запросу "${searchData.or_search_query}"</h1>`;
                    } else {
                        resultContainer.innerHTML = `<h1 class="tags_finder">Найдено ${searchData.found_news} результатов по запросу "${searchData.or_search_query}"</h1>`;
                    }

                    var newsContainer = document.createElement('div');
                    newsContainer.className = 'row';

                    searchData.news.forEach(function(newsItem) {
                        var displayedNews = [];

                        newsItem[3].forEach(function(tag) {
                            var tagWords = tag.toLowerCase().split();

                            tagWords.forEach(function(tagWord) {
                                if (tagWord.startsWith(searchData.search_query.toLowerCase()) && displayedNews.indexOf(newsItem) === -1) {
                                    var newsElement = document.createElement('div');
                                    newsElement.className = 'news-cont';
                                    newsElement.onclick = function() { handleContainerClick(newsItem[2]); };

                                    newsElement.innerHTML = `
                                        <img src="${newsItem[5]}" style="width: 100%; max-height: 275px;">
                                        <h4 class="news-title">${newsItem[1]}</h4>
                                        <h8 class="news-time">${newsItem[4]}</h8>
                                        <div class="tags-container">
                                            ${newsItem[3].map(function(newsTag) {
                                                return (newsTag === tag)
                                                    ? `<span class="found_tag" onclick="handleTagClick('${newsTag}')">${newsTag}</span>`
                                                    : `<span class="tag" onclick="handleTagClick('${newsTag}')">${newsTag}</span>`;
                                            }).join('')}
                                        </div>
                                    `;

                                    newsContainer.appendChild(newsElement);
                                    displayedNews.push(newsItem);
                                }
                            });
                        });
                    });

                    resultContainer.appendChild(newsContainer);

                    if (searchData.found_news === 1) {
                        resultContainer.classList.add('single-result');
                    } else {
                        resultContainer.classList.remove('single-result');
                    }
                })
                .catch(error => console.error('Ошибка:', error));
            }
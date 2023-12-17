fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        const newsContainer = document.getElementById('newsContainer');

        // Очищаем содержимое контейнера перед добавлением новых элементов
        newsContainer.innerHTML = '';

        // Проходим по массиву данных и добавляем элементы в контейнер
        data.forEach(newsItem => {
            // Создаем div-элемент для каждой новости
            const newsElement = document.createElement('div');
            newsElement.classList.add('news-cont');
            newsElement.addEventListener('click', () => handleContainerClick(newsItem[2]));

            // Создаем изображение
            const imageElement = document.createElement('img');
            imageElement.src = newsItem[5];
            imageElement.style.width = '100%';
            imageElement.style.maxHeight = '275px';
            newsElement.appendChild(imageElement);

            // Создаем заголовок
            const titleElement = document.createElement('h4');
            titleElement.classList.add('news-title');
            titleElement.textContent = newsItem[1];
            newsElement.appendChild(titleElement);

            // Создаем время
            const timeElement = document.createElement('h8');
            timeElement.classList.add('news-time');
            timeElement.textContent = newsItem[4];
            newsElement.appendChild(timeElement);

            // Создаем контейнер для тегов
            const tagsContainer = document.createElement('div');
            tagsContainer.classList.add('tags-container');

            // Проходим по тегам и создаем элементы span для каждого
            newsItem[3].forEach(newsTag => {
                const tagElement = document.createElement('span');
                tagElement.classList.add('tag');
                tagElement.textContent = newsTag;
                tagElement.addEventListener('click', () => handleTagClick(newsTag));
                tagsContainer.appendChild(tagElement);
            });

            newsElement.appendChild(tagsContainer);

            // Добавляем созданный элемент в основной контейнер
            newsContainer.appendChild(newsElement);
        });
    })
    .catch(error => console.error('Ошибка при получении данных:', error));
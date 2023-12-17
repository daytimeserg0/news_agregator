function handleContainerClick(link) {
        var selection = window.getSelection();
        if (!selection.toString()) {
            // Выполнить переход по ссылке только если нет выделенного текста
            window.location.href = link;
        }
    }

    function handleTagClick(tag) {
        var selection = window.getSelection();
        if (!selection.toString()) {
            event.stopPropagation(); // Предотвращение всплытия события только при отсутствии выделенного текста
            var searchText = tag;

            const isDarkMode = document.body.classList.contains("dark");

            window.location.href = 'tag-news?tag=' + encodeURIComponent(searchText);
        }
    }
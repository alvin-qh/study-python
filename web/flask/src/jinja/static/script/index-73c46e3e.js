const $timer = $('.timer');

$timer.textContent = new Date().toLocaleString();
setInterval(() => {
  $timer.textContent = new Date().toLocaleString();
}, 1000);

const $searchText = $('.search-box input[type=text]');
const $searchBtn = $('.search-box button');
const $searchResult = $('.search-result');

$searchBtn.addEventListener('click', async () => {
  const keyword = $searchText.value.trim();

  if (keyword) {
    const res = await fetch(`/api/search?key=${encodeURIComponent(keyword)}`, {
      method: 'GET',
    });

    if (res) {
      const data = await res.json();
      if (data && data.results) {
        data.results.forEach(r => {
          const $result = document.createElement('div');
          $result.classList.add('item');
          $result.innerHTML = `
            <div class="title">${r.title}</div>
            <div class="description">${r.description}</div>
            <div class="link"><a href="${r.url}">${r.url}</a></div>
          `;
          $searchResult.appendChild($result);
        });
      }
    }

    $searchText.select();
  }
});

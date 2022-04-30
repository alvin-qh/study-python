;
(() => {
  function main() {
    const $links = document.querySelectorAll('.lang-block > a');
    for (const $link of $links) {
      $link.addEventListener('click', e => {
        e.preventDefault();
        const $elem = e.currentTarget;
        const lang = $elem.getAttribute('data-lang');
        location.href = `?lang=${lang}`;
      }, false);
    }
  }

  const $main = document.querySelector('div.main');
  if ($main.id === 'index') {
    main();
  }
})();

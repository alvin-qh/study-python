;
(function () {
  const $nameText = document.getElementsByName('name')[0];
  const $searchButton = document.getElementsByClassName('search-button')[0];

  $searchButton.addEventListener('click', () => {
    location.href = `/?kwd=${$nameText.value}`;
  });

  const $formChange = document.querySelector('form.change');
  const $formDelete = document.querySelector('form.delete');
  $formDelete.actionTemplate = $formDelete.action;

  for (const $td of document.getElementsByTagName('td')) {
    const $content = $td.querySelector('.content');
    const $close = $td.querySelector('.close');

    $content.addEventListener('click', e => {
      const $elem = e.currentTarget;
      if (!$elem.editor) {
        const val = $elem.innerText;

        const $input = document.createElement('input');
        $input.type = 'text';
        $input.value = val;
        $input.srcValue = val;

        $elem.innerHTML = '';
        $elem.append($input);

        $input.select();
        $input.focus();

        $elem.editor = $input;
      } else {
        $formChange.querySelector('input[name=old_value]').value = $elem.editor.srcValue;
        $formChange.querySelector('input[name=new_value]').value = $elem.editor.value;
        $formChange.submit();
      }
    }, false);

    $close.addEventListener('click', e => {
      e.preventDefault();
      $formDelete.action = $formDelete.actionTemplate.replace('{0}', $content.innerText);
      $formDelete.submit();
    }, false);
  }
})();

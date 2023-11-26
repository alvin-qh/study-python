import './main.scss';

import logo from './logo.png';


const $app = document.querySelector('#app')!;

const $nav = document.createElement('nav');
$nav.classList.add('logo');
$app.appendChild($nav);

const $img = document.createElement('img');
$img.src = logo;
$nav.appendChild($img);

const $h1 = document.createElement('h1');
$h1.textContent = 'Hello World';
$app.appendChild($h1);

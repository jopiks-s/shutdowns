day_index = new URLSearchParams(window.location.search).get('day_index');
day_index = parseInt(day_index) + 1;
document.querySelectorAll(`table tr td:nth-child(${day_index})`).forEach(c => {
    c.style.borderLeft = '2px solid #FFE500';
    c.style.borderRight = '2px solid #FFE500';
});
document.querySelectorAll(`table tr td:nth-child(${day_index-1})`).forEach(c => {
    c.style.borderLeft = 'none';
});
document.querySelectorAll(`table tr td:nth-child(${day_index+1})`).forEach(c => {
    c.style.borderRight = 'none';
});
document.querySelectorAll(`thead tr th:nth-child(${day_index})`).forEach(c => {
    c.style.backgroundColor = '#ffe500';
});

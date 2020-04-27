const formattedDate = date => (
  date.toLocaleDateString('pt-BR')
      .split('/')
      .map(val => val.padStart(2, '0'))
      .join('/')
);

const formattedTime = date => {
  var hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}${ampm}`;
};

const filters = {
  titleCase: value => (
    value.replace(
          /([a-z])([A-Z])/g,
          (allMatches, firstMatch, secondMatch) =>  (firstMatch + " " + secondMatch),
        )
        .toLowerCase()
        .replace(
          /([ -_]|^)(.)/g,
          (allMatches, firstMatch, secondMatch) => ((firstMatch ? " " : "") + secondMatch.toUpperCase()),
        )
  ),

  date: value => {
    if (!value) { return '-'; }

    try {
      return formattedDate(new Date(value));
    } catch (_) {
      return value ;
    }
  },

  time: value => {
    if (!value) { return '-'; }

    try {
      return formattedTime(new Date(value));
    } catch (_) {
      return value ;
    }
  },

  datetime: value => {
    if (!value) { return '-'; }

    try {
      const date = new Date(value);
      const dateStr = formattedDate(date);
      const timeStr = formattedTime(date);
      return `${dateStr} - ${timeStr}`;
    } catch (_) {
      return value;
    }
  },
};

const OBDFilters = {
  install(Vue) {
    Object.keys(filters).forEach(key => {
      Vue.filter(key, filters[key]);
    });
  }
};

export default OBDFilters;

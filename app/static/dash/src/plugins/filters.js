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
    if (!value) { return ''; }

    try {
      const zeroed = val => (val < 10 ? `0${val}` : val);
      return value.toLocaleDateString('pt-BR').split('/').map(val => zeroed(val)).join('/');
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

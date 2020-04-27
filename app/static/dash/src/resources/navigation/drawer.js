export default {
  auth: [
    {
      icon: 'mdi-view-dashboard',
      label: 'Control Panel',
      route: { name: 'Dashboard' },
    },
    {
      icon: 'mdi-gas-station',
      label: 'Fuel Analysis',
      route: { name: 'Fuel' },
    },
  ],
  unauth: [
    {
      icon: 'mdi-home',
      label: 'Home',
      route: { name: 'Index' },
    },
  ],
};

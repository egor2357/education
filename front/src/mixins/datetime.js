import moment from "moment";

export default {
  methods: {
    formatTime(time) {
      return moment(time, "HH:mm:ss").format("HH:mm");
    },
    timeMask(value) {
      let hours = [
        /[0-2]/,
        value.charAt(0) === '2' ? /[0-3]/ : /[0-9]/,
      ];
      let minutes = [/[0-5]/, /[0-9]/];
      return value.length > 2
        ? [...hours, ':', ...minutes]
        : hours;
    },
  },


};

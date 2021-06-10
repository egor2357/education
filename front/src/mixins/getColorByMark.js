export default {
  methods: {
    getColorByMark(mark){
      if (mark===0) {
        return "#ff1f1f";
      } else if (mark===1) {
        return "#f2ef0f";
      } else if (mark===2) {
        return "#00ac00";
      } else {
        return "#ccc";
      }
    },
  },
};

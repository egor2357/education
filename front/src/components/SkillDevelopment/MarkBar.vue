<template>
    <div class='mark-bar' :style='`width: ${width * 100}%; background-color:rgb(${color.toString()}) `'></div>
</template>

<script>
export default {
name: 'MarkBar',
  props: {
    value: {
      type: Number,
      default: NaN
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      colorStart: [255, 80, 80],
      colorsMiddle: [255, 255, 80],
      colorsEnd: [80, 255, 80]
      // colorStart: [255, 0, 0],
      // colorsMiddle: [255, 255, 0],
      // colorsEnd: [0, 255, 0]
    };
  },
  computed: {
    width(){
      return isNaN(this.value) ? .5 : Math.max(this.min, this.value)/this.max;
    },
    percent() {
      const diff = this.max - this.min;
      const diffVal = Math.max(this.value, this.min) - this.min;
      return diffVal / diff;
    },
    color() {
      if (isNaN(this.value))
        return [230, 230, 230];
      if (this.percent <= 0.5) {
        return this.getColorsDiff(this.colorStart, this.colorsMiddle, this.percent * 2);
      } else {
        return this.getColorsDiff(this.colorsMiddle, this.colorsEnd, (this.percent - 0.5) * 2);
      }
    }
  },

  methods: {
    getColorsDiff(color1, color2, percent) {
      return [color1[0] + (color2[0] - color1[0]) * percent,
        color1[1] + (color2[1] - color1[1]) * percent,
        color1[2] + (color2[2] - color1[2]) * percent];
    }
  }
};
</script>

<style lang="sass" scoped>
.mark-bar 
  height: 15px
  border-radius: 6px
  transition: width .35s ease
  margin: 5px
  box-shadow: 0 0 2px 1px rgba(0,0,0,.15)  
</style>
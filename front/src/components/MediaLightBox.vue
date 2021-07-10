<template>
  <LightBox
    :media="media"
    :showCaption="false"
    :showThumbs="false"
    :showLightBox="true"
    :startAt="startAt"
    @onClosed="$emit('close')"
  >
  </LightBox>
</template>

<script>
import LightBox from "vue-it-bigger";
import("vue-it-bigger/dist/vue-it-bigger.min.css");
export default {
  name: "MediaLightBox",
  components: {
    LightBox,
  },
  props: {
    files: {
      type: Array,
      default: () => {
        return [];
      },
    },
    selectedFile: {
      type: Object,
      default: () => {
        return { uid: null };
      },
    },
  },
  data() {
    return {
      startAt: 0,
    };
  },
  computed: {
    media() {
      let arr = [];
      this.files.forEach((file, index) => {
        if (file.photo) {
          arr.push({
            type: "image",
            thumb: file.thumbUrl ? file.thumbUrl : file.url,
            src: file.url,
            name: file.name,
          });
          if (this.selectedFile.uid === file.uid) {
            this.startAt = arr.length - 1;
          }
        }
      });
      return arr;
    },
  },
};
</script>

<style scoped></style>

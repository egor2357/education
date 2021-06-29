<template>
  <LightBox
    :media="media"
    :showCaption="false"
    :showLightBox="true"
    :startAt="startAt"
    @onClosed="$emit('close')"
  >
    <template v-slot:customCaption="slotProps">
      <a-button icon="save" @click="downloadFile(slotProps.currentMedia)">
      </a-button>
    </template>
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
            thumb: file.thumbUrl !== null ? file.thumbUrl : file.url,
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
  methods: {
    async downloadFile(media) {
      let url = media.src;
      if (process.env.NODE_ENV === "development") {
        url = url.split("http://192.168.137.100:8001")[1];
      }
      let name = media.name;
      let response = await this.$axios.get(url);
      let blob = new Blob([response.data], {
        type: response.headers["content-type"],
      });
      let link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = name;
      link.click();
    },
  },
};
</script>

<style scoped></style>

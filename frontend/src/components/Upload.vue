// Upload.vue // following https://github.com/alessiomaffeis/vue-picture-input-example
<template>
  <div>
    <p>Upload</p>

    <picture-input ref="pictureInput" @change="onChange" @remove="onRemove" width="200" height="200" margin="8" accept="image/jpeg,image/png" size="10"
      :removable="true" :customStrings="{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a GIF'
      }">
    </picture-input>

    <button @click="getName">Identify pet</button><br>
    Pet name: {{ petName }}{{ progress }}
  </div>
</template>

<script>
  import PictureInput from 'vue-picture-input'
  import axios from 'axios'
//  import pets from 'pets'  //new 3/7 KER

  export default {
    name: 'app',
    data() {
      return {
        petName: "",
        progress: ""
      }
    },
    components: {
      PictureInput
    },
    methods: {
      sendUploadToBackend(name, data) {
        const path = 'http://localhost:5000/api/upload'
        axios.post(path, {'name': name, 'data': data})
        console.log('got data from api/upload')
      },

    getName () {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.petName = this.getPetNameFromBackend()
    },
    getPetNameFromBackend () {
      var progressRun = setInterval(() => {this.progress += '.'}, 500)
      const path = `http://localhost:5000/api/name`
      axios.get(path)
      .then(response => {
//        this.petName = response.data.petName // need to put that in JSON probably.
          this.petName = response.data.petName
          clearInterval(progressRun)
          this.progress = ''
      })
      .catch(error => {
        console.log(error)
        clearInterval(progressRun)
        this.progress = ''
      })
    },
    onChange(image) {
      console.log('New picture selected!')
      this.petName = ''
      if (this.$refs.pictureInput.image) {
        console.log('Picture is loaded.')
        this.sendUploadToBackend(this.$refs.pictureInput.file.name, this.$refs.pictureInput.image) 
        this.getPetNameFromBackend()
      } else {
        console.log('FileReader API not supported: use the <form>, Luke!')
      }
    },
    onRemove() {
      this.petName = ''

      var path = `http://localhost:5000/api/remove`
      axios.delete(path)
      .then(response => {
        console.log(response.data.message)
      })
      .catch(error => {
        console.log(error.data)
      })
    }
    },
  created () {
    // this.getName()
  }
}

</script>

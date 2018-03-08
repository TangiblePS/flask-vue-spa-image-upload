// Upload.vue // following https://github.com/alessiomaffeis/vue-picture-input-example
<template>
  <div>
    <p>Upload</p>

    <picture-input ref="pictureInput" @change="onChange" width="200" height="200" margin="8" accept="image/jpeg,image/png" size="10"
      :removable="true" :customStrings="{
        upload: '<h1>Bummer!</h1>',
        drag: 'Drag a GIF'
      }">
    </picture-input>

    <button @click="getName">Identify pet</button><br>
    Pet name: {{ petName }} 
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
	  petName: ""
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
       const path = `http://localhost:5000/api/name`
       axios.get(path)
       .then(response => {
//        this.petName = response.data.petName // need to put that in JSON probably.
          this.petName = response.data.petName
       })
       .catch(error => {
         console.log(error)
       })
     },
     onChange(image) {
       console.log('New picture selected!')
       if (this.$refs.pictureInput.image) {
         console.log('Picture is loaded.')
         this.sendUploadToBackend(this.$refs.pictureInput.file.name, this.$refs.pictureInput.image) 
       } else {
         console.log('FileReader API not supported: use the <form>, Luke!')
       }
     }
    },
  created () {
    this.getPetName()
  }
}

</script>

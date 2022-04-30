<template>
    <div class="form-inline">
        <div class="input-group col-10 offset-1">
            <label for="input-name" class="sr-only">Name: </label>
            <input class="form-control" type="text" id="input-name" :placeholder="text" v-model="keyWord"/>
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="button" @click="doSearch">{{ text }}</button>
            </div>
        </div>
    </div>
</template>

<script>
    import _ from "lodash";
    import axios from "axios";

    export default {
        props: {
            text: [String]
        },
        data() {
            return {
                keyWord: ''
            }
        },
        methods: {
            doSearch() {
                const keyWord = _.trim(this.keyWord);
                if (keyWord) {
                    axios
                        .get('/api/search', {
                            params: {
                                key: keyWord
                            }
                        })
                        .then(resp => {
                            if (resp.status !== 200) {
                                console.error(resp.statusText);
                                return {};
                            }
                            return resp.data;
                        })
                        .then(data => {
                            this.$emit('input', data.results || [])
                        });
                }
            }
        }
    }
</script>

<style lang="less" scoped>
</style>
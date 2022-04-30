import {ns, Vue} from "../common/common";
import moment from "moment";

import NameInput from "./comps/name-input";
import SearchResult from "./comps/search-result";

ns('home.index', function () {
    new Vue({
        components: {NameInput, SearchResult},
        el: '#app',
        data: {
            currentTime: '',
            searchResults: []
        },
        methods: {
            changeCurrentTime() {
                const now = moment();
                this.currentTime = now.format('YYYY-MM-DD HH:mm:ss')
            }
        },
        mounted() {
            this.changeCurrentTime();
            setInterval(() => {
                this.changeCurrentTime();
            }, 1000)
        }
    });
});
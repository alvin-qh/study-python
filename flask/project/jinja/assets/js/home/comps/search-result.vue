<template>
    <div>
        <div v-if="!hasResult">
            <div>No result found</div>
        </div>
        <template v-else v-for="result in results">
            <div class="title">{{ result.title }}</div>
            <div class="description">{{ result.description }}</div>
            <div class="url">
                <a :href="result.url" target="_blank">{{ result.url }}</a>
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        props: {
            text: [String],
            results: [Array]
        },
        computed: {
            hasResult() {
                return this.results && this.results.length > 0
            }
        }
    }
</script>

<style lang="less" scoped>
    .title {
        font-size: 16px;
        font-weight: bold;
    }

    .description {
        font-size: 14px;
        color: #9a9a9a;
    }
</style>
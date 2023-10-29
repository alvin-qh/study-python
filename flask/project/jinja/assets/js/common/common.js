import "../../css/common/main.less";
import SrcVue from "vue";

export function ns(namespace, func) {
    let root = window;
    const parts = namespace.split('.');
    for (let i = 0; i < parts.length - 1; i++) {
        const n = parts[i];
        if (!root[n]) {
            root[n] = {};
        }
        root = root[n];
    }
    const n = parts[parts.length - 1];
    root[n] = func;
}


export const Vue = SrcVue.extend({
    delimiters: ['${', '}']
});
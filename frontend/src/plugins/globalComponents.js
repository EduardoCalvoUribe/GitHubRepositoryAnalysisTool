import Badge from "../components/Badge.vue";
import BaseAlert from "../components/BaseAlert.vue";
import BaseButton from "../components/BaseButton.vue";
import BaseCheckbox from "../components/BaseCheckbox.vue";
import BaseInput from "../components/BaseInput.vue";
import BasePagination from "../components/BasePagination.vue";
import BaseProgress from "../components/BaseProgress.vue";
import BaseRadio from "../components/BaseRadio.vue";
import BaseSlider from "../components/BaseSlider.vue";
import BaseSwitch from "../components/BaseSwitch.vue";
import Card from "../components/Card.vue";
import Icon from "../components/Icon.vue";

export default {
  install(Vue) {
    Vue.component(Badge.name, Badge);
    Vue.component(BaseAlert.name, BaseAlert);
    Vue.component(BaseButton.name, BaseButton);
    Vue.component(BaseInput.name, BaseInput);
    Vue.component(BaseCheckbox.name, BaseCheckbox);
    Vue.component(BasePagination.name, BasePagination);
    Vue.component(BaseProgress.name, BaseProgress);
    Vue.component(BaseRadio.name, BaseRadio);
    Vue.component(BaseSlider.name, BaseSlider);
    Vue.component(BaseSwitch.name, BaseSwitch);
    Vue.component(Card.name, Card);
    Vue.component(Icon.name, Icon);
  }
};

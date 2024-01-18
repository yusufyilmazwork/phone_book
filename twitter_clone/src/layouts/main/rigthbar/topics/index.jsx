import {topics} from "../../../../utils/const.jsx";
import Topic from "../../../../layouts/main/rigthbar/topics/topic";
import SidebarSection from "../../../../components/sidebar-section";

export default function Topics() {
	return (
		<SidebarSection
			title="İlgini çekebilecek gündemler"
			more="/trends"
		>
			{topics.map((topic, index) => <Topic item={topic} key={index}/>)}
		</SidebarSection>
	)
}
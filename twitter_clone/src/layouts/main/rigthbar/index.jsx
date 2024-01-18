import Search from "../../../layouts/main/rigthbar/search";

import Premium from "../../../layouts/main/rigthbar/premium";
import Topics from "../../../layouts/main/rigthbar/topics";
import WhoFollow from "../../../layouts/main/rigthbar/who-follow";
import Footer from "../../../layouts/main/rigthbar/footer";

export default function RightBar() {
	return (
		<aside className="w-[350px] mr-2.5">
			<Search />
			<Premium />
			<Topics />
			<WhoFollow />
			<Footer />
		</aside>
	)
}
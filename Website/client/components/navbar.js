import Image from "next/image"

export default function Navbar(){

	return (
		<div className="w-full flex items-center justify-center gap-4 p-4 text-2xl font-semibold shadow-md">
			<div className="flex items-center justify-center gap-1 ">
				<div className="w-12 aspect-square relative ">
					<Image src="/NITK_logo.png" fill />
				</div>
				<p>NIT Surathkal</p>
			</div>

			<div className="w-1 bg-black h-10">
			</div>

			<div>
				Course Recommendation
			</div>
		</div>
	)
}
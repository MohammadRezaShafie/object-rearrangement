from manim import *
import os
import time

class MainSequence(Scene):
    def play_videos(self, pre_frames_folder, post_frames_folder, sc, seg = 0):
        # Load and sort frames from both folders
        pre_frames = sorted([
            os.path.join(pre_frames_folder, frame)
            for frame in os.listdir(pre_frames_folder)
            if frame.endswith(".jpg")
        ], key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1]))

        post_frames = sorted([
            os.path.join(post_frames_folder, frame)
            for frame in os.listdir(post_frames_folder)
            if frame.endswith(".jpg")
        ], key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1]))
        
        # Create ImageMobjects for each frame
        if seg == 0:
            pre_frame_objects = [ImageMobject(frame).move_to(ORIGIN + LEFT * 2).scale(sc) for frame in pre_frames]
            post_frame_objects = [ImageMobject(frame).move_to(ORIGIN + RIGHT * 2).scale(sc) for frame in post_frames]
        elif seg == 1:
            pre_frame_objects = [ImageMobject(frame).move_to(ORIGIN + RIGHT * 0.0).scale(sc) for frame in pre_frames]
            post_frame_objects = [ImageMobject(frame).move_to(ORIGIN + RIGHT * 4.5).scale(sc) for frame in post_frames]
                   
        return pre_frame_objects, post_frame_objects
    
       
    def construct(self):

        lab_logo = ImageMobject("lab_logo.png").scale(1.4)
        lab_logo.move_to(ORIGIN + LEFT * 2)
        ut_logo = ImageMobject("ut_logo.png").scale(0.26)
        ut_logo.move_to(ORIGIN + RIGHT * 2)
        self.play(FadeIn(lab_logo),FadeIn(ut_logo), run_time=1)
        self.wait(0.5)
        

        self.play(
            lab_logo.animate.scale(0.57).to_corner(DL),
            ut_logo.animate.scale(0.57).to_corner(DR),
            run_time=2
        )


        title = Text(
            "AI-Driven Relocation Tracking in\n Dynamic Kitchen Environments",
            font_size=52,
            t2c={"Relocation Tracking": "#3498db"}
        ).move_to(ORIGIN + UP * 3)
        
        authors = VGroup(
            Text("Arash Nasr Esfahani",  font_size=26),
            Text("Hamed Hosseini",  font_size=26),
            Text("Mehdi Tale Masouleh",  font_size=26),
            Text("Ahmad Kalhor",  font_size=26),
            Text("Hedieh Sajedi",  font_size=26),
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN * 2.5)
    
        institutes = VGroup(  
            Text("Human and Robot Interaction Lab, School of Electrical and Computer Engineering,\n                                                                              University of Tehran", t2c={"Human and Robot Interaction Lab": "#3498db"},  font_size=21)
        ).arrange(DOWN, buff=0.3).next_to(authors, DOWN * 1.5)
        
        self.play(Write(title), run_time=1)
        self.play(
            FadeIn(authors),
            run_time=2
        )

        self.play(
            FadeIn(institutes),
            run_time=2
        )        

        self.play(
            FadeOut(title),
            FadeOut(institutes),
            FadeOut(authors),
            run_time=1
        )


        nav_title = Text("Agent Navigation", font_size=48).to_edge(UP)
        self.play(Write(nav_title), run_time=1)
        

        video_box_1 = Rectangle(height=5, width=5).move_to(ORIGIN + LEFT * 2).scale(0.7)
        video_box_2 = Rectangle(height=5, width=5).move_to(ORIGIN + RIGHT * 2).scale(0.7)
        pre_label = Text("Pre-Change", font_size=28).move_to(video_box_1.get_center() + UP * 2)
        post_label = Text("Post-Change", font_size=28).move_to(video_box_2.get_center() + UP * 2)


        self.play(
            Create(video_box_1),
            Create(video_box_2),
            Write(pre_label),
            Write(post_label),
            run_time=1
        )

        pre_frames, post_frames = self.play_videos("I:/TAAR/8 - ICCKE/6 - Detections/frames_12", "I:/TAAR/8 - ICCKE/6 - Detections/frames_8", 0.6)

        for i in range(min(len(pre_frames), int(5/0.2))):  # 5 seconds of video
            if i < len(pre_frames):
                self.add(pre_frames[i])
            if i < len(post_frames):
                self.add(post_frames[i])
            self.wait(0.2)
            if i < len(pre_frames):
                self.remove(pre_frames[i])
            if i < len(post_frames):
                self.remove(post_frames[i])

        pre_pic = ImageMobject("I:/TAAR/8 - ICCKE/6 - Detections/frames_12/25").scale(1.0)
        pre_pic.move_to(ORIGIN + LEFT * 2).scale(0.6)
        self.add(pre_pic)    

        post_pic = ImageMobject("I:/TAAR/8 - ICCKE/6 - Detections/frames_8/25").scale(1.0)
        post_pic.move_to(ORIGIN + RIGHT * 2).scale(0.6)
        self.add(post_pic)       
              
        self.play(
            video_box_1.animate.shift(LEFT * 2.5),
            video_box_2.animate.shift(LEFT * 2.5),
            pre_pic.animate.shift(LEFT * 2.5),
            post_pic.animate.shift(LEFT * 2.5),
            pre_label.animate.shift(LEFT * 2.5),
            post_label.animate.shift(LEFT * 2.5),
            run_time=2
        )

        all_elements = VGroup(video_box_1, video_box_2, pre_label, post_label)
        bracket = Brace(all_elements, RIGHT)
        yolo_box = Rectangle(height=2.25, width=3.5).next_to(bracket, RIGHT * 2, buff=0.5)
        yolo_text = Text("Object Detection Model", font_size=24).move_to(yolo_box.get_center() + UP * 1.4)
        yolo_pic = ImageMobject("detect.png").scale(1.0)
        yolo_pic.move_to(yolo_box).scale(0.5)
        arrow_to_yolo = Arrow(bracket.get_right(), yolo_box.get_left(), buff=0.1)
        
        self.play(
            FadeIn(bracket),
            FadeIn(arrow_to_yolo),
            Create(yolo_box),
            Write(yolo_text),
            FadeIn(yolo_pic),
            run_time=2
        )
        
        self.play(

            FadeOut(video_box_1),
            FadeOut(video_box_2),
            FadeOut(pre_pic),
            FadeOut(post_pic),
            FadeOut(pre_label),
            FadeOut(post_label),
            FadeOut(arrow_to_yolo),
            FadeOut(bracket),
            yolo_box.animate.shift(LEFT * 9.25),
            yolo_text.animate.shift(LEFT * 9.25),
            yolo_pic.animate.shift(LEFT * 9.25),
            Transform(nav_title, Text("Object Detection", font_size=48).to_edge(UP)),
            run_time=3
        )



        video_box_1 = Rectangle(height=5, width=5).move_to(ORIGIN + RIGHT * 0.0).scale(0.7)
        video_box_2 = Rectangle(height=5, width=5).move_to(ORIGIN + RIGHT * 4.5).scale(0.7)
        pre_label = Text("Pre-Change", font_size=28).move_to(video_box_1.get_center() + UP * 2)
        post_label = Text("Post-Change", font_size=28).move_to(video_box_2.get_center() + UP * 2)
        all_elements = VGroup(video_box_1, video_box_2, pre_label, post_label)
        bracket = Brace(all_elements, LEFT)
        arrow_to_detection_videos= Arrow(yolo_box.get_right(), bracket.get_left(), buff=0.1)
        
        self.play(
            FadeIn(bracket),
            FadeIn(arrow_to_detection_videos),
            run_time=1  
        )

        
        self.play(
            Create(video_box_1),
            Create(video_box_2),
            Write(pre_label),
            Write(post_label),
            run_time=2  
        )
            
        pre_frames, post_frames = self.play_videos("I:/TAAR/8 - ICCKE/6 - Detections/detections_12", "I:/TAAR/8 - ICCKE/6 - Detections/detections_8", 0.6, 1)

        for i in range(min(len(pre_frames), int(5/0.2))):  # 5 seconds of video
            if i < len(pre_frames):
                self.add(pre_frames[i])
            if i < len(post_frames):
                self.add(post_frames[i])
            self.wait(0.2)
            if i < len(pre_frames):
                self.remove(pre_frames[i])
            if i < len(post_frames):
                self.remove(post_frames[i])

        pre_pic = ImageMobject("I:/TAAR/8 - ICCKE/6 - Detections/detections_12/25").scale(1.0)
        pre_pic.move_to(ORIGIN + RIGHT * 0.0).scale(0.6)
        self.add(pre_pic)    

        post_pic = ImageMobject("I:/TAAR/8 - ICCKE/6 - Detections/detections_8/25").scale(1.0)
        post_pic.move_to(ORIGIN + RIGHT * 4.5).scale(0.6)
        self.add(post_pic)       
        
        self.play(
            FadeOut(bracket),
            FadeOut(arrow_to_detection_videos),
            FadeOut(yolo_box),
            FadeOut(yolo_text),
            FadeOut(yolo_pic),
            run_time=1.5
        )
        
        # 11. Change title to "Relocation Tracking"
        self.play(
            Transform(nav_title, Text("Relocation Tracking", font_size=48).to_edge(UP)),
            video_box_1.animate.scale(0.7).shift(LEFT * 5),
            video_box_2.animate.scale(0.7).shift(LEFT * 6),
            pre_pic.animate.scale(0.7).shift(LEFT * 5),
            post_pic.animate.scale(0.7).shift(LEFT * 6),
            pre_label.animate.scale(0.7).shift(LEFT * 5 + DOWN * 0.4 ),
            post_label.animate.scale(0.7).shift(LEFT * 6 + DOWN* 0.4),
            run_time=4
        )
        
        # 12. Add depth data section
        plus_sign = Text("+", font_size=36).move_to(video_box_2.get_center() + RIGHT * 1.75)
        depth_box = Rectangle(height=1, width=2).next_to(plus_sign, RIGHT * 1.75)
        depth_pic = ImageMobject("depth.png").scale(1.0)
        depth_pic.move_to(depth_box.get_center()).scale(0.35)
        depth_text = Text("Depth Data", font_size=24).move_to(depth_box.get_center() + UP * 1.0)
        
        self.play(
            Write(plus_sign),
            Create(depth_box),
            Write(depth_text),
            FadeIn(depth_pic), 
            run_time=2
        )
        

        self.play(
            Group(video_box_1, video_box_2, pre_label, post_label, pre_pic, post_pic, depth_box, depth_pic, depth_text, plus_sign).animate.scale(0.75).shift(LEFT * 1.5),
            run_time=2
        )
        all_elements = Group(video_box_1, video_box_2, pre_label, post_label, pre_pic, post_pic, depth_box, depth_pic, depth_text)
        bracket = Brace(all_elements, RIGHT)
        arrow_to_algo = Arrow(bracket.get_right(), bracket.get_right() + RIGHT * 1.25, buff=0.1)
        algo_box = Rectangle(height=1.75, width=3.5).next_to(arrow_to_algo, RIGHT * 1.66)
        algo_text = Text("Best-Associated Frame\n    Selection Algorithm", font_size=21).next_to(arrow_to_algo, RIGHT * 2.7)

        
        
        self.play(
            FadeIn(bracket),
            FadeIn(arrow_to_algo),
            Create(algo_box),
            Write(algo_text),
            run_time=2
        )
        
        self.play(
            FadeOut(bracket),
            FadeOut(arrow_to_algo),
            FadeOut(video_box_1),
            FadeOut(video_box_2),
            FadeOut(pre_label),
            FadeOut(post_label),
            FadeOut(pre_pic),
            FadeOut(post_pic),
            FadeOut(depth_box),
            FadeOut(depth_pic),
            FadeOut(depth_text),
            FadeOut(plus_sign),
            run_time=2
        )
        
        self.play(
        algo_box.animate.shift(LEFT * 9 + DOWN * 0.27),
        algo_text.animate.shift(LEFT * 9 + DOWN * 0.27),
        run_time=2  
        )
        
        best_box_1 = Rectangle(height=5, width=5).move_to(ORIGIN + RIGHT * 0.0).scale(0.7)
        best_box_2 = Rectangle(height=5, width=5).move_to(ORIGIN + RIGHT * 4.5).scale(0.7)  
        box_label = Text("Best-Associated Frames for     ", font_size=24, t2c={"Apple": "#3498db"}).move_to((best_box_1.get_center() + best_box_2.get_center())/2 + UP * 2.25 + LEFT * 0.45)
        box_obj = Text("                            Apple", font_size=24, t2c={"Apple": "#3498db"}, weight=BOLD).move_to(box_label.get_center() + RIGHT * 2.57)
        best_to_samples = Arrow(algo_box.get_right(), best_box_1.get_left(), buff=0.1)

        self.play(
            Create(best_box_1),
            Create(best_box_2),
            Create(best_to_samples),
            Write(box_obj),
            Write(box_label),
            run_time=1.5
        )
        
        pre_pic = ImageMobject("101.png").scale(1.0)
        pre_pic.move_to(ORIGIN + RIGHT * 0.0).scale(0.6)
        self.add(pre_pic)    

        post_pic = ImageMobject("165.png").scale(1.0)
        post_pic.move_to(ORIGIN + RIGHT * 4.5).scale(0.6)
        self.add(post_pic)      

        self.play(
            FadeIn(pre_pic),
            FadeIn(post_pic),
            run_time=0.8
        )     

                  
        self.wait(2)            
        self.play(
            FadeOut(box_obj),
            FadeOut(pre_pic),
            FadeOut(post_pic),
            run_time=2
        )

        box_obj = Text("                            Mug", font_size=24, t2c={"Mug": "#3498db"}, weight=BOLD).move_to(box_label.get_center()+ RIGHT * 2.53 + DOWN * 0.03)
        pre_pic = ImageMobject("78.png").scale(1.0)
        pre_pic.move_to(ORIGIN + RIGHT * 0.0).scale(0.6)
   

        post_pic = ImageMobject("16.png").scale(1.0)
        post_pic.move_to(ORIGIN + RIGHT * 4.5).scale(0.6)    
   
        self.play(
            FadeIn(box_obj),
            FadeIn(pre_pic),
            FadeIn(post_pic),
            run_time=0.8
        )     

        self.wait(2)            
        self.play(
            FadeOut(box_obj),
            FadeOut(pre_pic),
            FadeOut(post_pic),
            run_time=2
        )     
        
        box_obj = Text("                            Bread", font_size=24, t2c={"Bread": "#3498db"}, weight=BOLD).move_to(box_label.get_center()+ RIGHT * 2.6)
        pre_pic = ImageMobject("107.png").scale(1.0)
        pre_pic.move_to(ORIGIN + RIGHT * 0.0).scale(0.6)  

        post_pic = ImageMobject("74.png").scale(1.0)
        post_pic.move_to(ORIGIN + RIGHT * 4.5).scale(0.6)
          
    
        self.play(
            FadeIn(box_obj),
            FadeIn(pre_pic),
            FadeIn(post_pic),
            run_time=2
        )     

    
        self.wait(2)
        self.play(
            FadeOut(box_obj),
            FadeOut(algo_box),
            FadeOut(algo_text),
            FadeOut(best_box_1),
            FadeOut(best_box_2),
            FadeOut(pre_pic),
            FadeOut(post_pic),
            FadeOut(best_to_samples),
            FadeOut(box_label),
            run_time=2
        )
        
        final_title = Text("Final Results", font_size=48).to_edge(UP)
        result_text = VGroup(
            Text("Apple has moved from frame 101 to 165.",  font_size=28, t2c={"Apple": "#3498db"}),
            Text("Mug has moved from frame 78 to 16.",  font_size=28, t2c={"Mug": "#3498db"}),
            Text("Bread has moved from frame 107 to 74.",  font_size=28, t2c={"Bread": "#3498db"}),
        ).arrange(DOWN, buff=0.3).next_to(final_title, DOWN * 3)
        
        self.play(
            Transform(nav_title, final_title),
            Write(result_text),
            run_time=1.5
        )

        self.wait(2)
        # 16. Final logo sequence
        self.play(
            FadeOut(Group(*[m for m in self.mobjects if (m != lab_logo or m != ut_logo)])),
            lab_logo.animate.move_to(ORIGIN + LEFT * 2).scale(1.65),
            ut_logo.animate.move_to(ORIGIN + RIGHT * 2).scale(1.65),
            run_time=2
        )
        
        self.play(FadeOut(lab_logo), FadeOut(ut_logo), run_time=1)
        self.wait(1)

if __name__ == "__main__":
    with tempconfig({
        "quality": "high_quality",
        "media_dir": "./media",
        "video_dir": "./media/videos",
    }):
        scene = MainSequence()
        scene.render()
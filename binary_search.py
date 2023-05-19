from manim import *

class BinarySearch(Scene):
    def construct(self):
        # Sorted array
        arr = list(range(11))
        target = 10

        # Create array visual
        rects, labels = self.create_array_visual(arr)
        
        # Create text for the target at the top of the scene
        target_text = Text(f"Target: {target}").scale(1.25).to_edge(UP)
        self.play(Write(target_text))


        # Perform binary search
        self.binary_search_visualization(rects, labels, arr, target)

    def create_array_visual(self, arr):
        rects = VGroup()
        labels = VGroup()
        for i in range(len(arr)):
            # Create squares instead of rectangles
            rect = Square(side_length=1.0, fill_opacity=1, fill_color=BLUE)
            rects.add(rect)
        rects.arrange(buff=0.2)  # Reduce the width of each box
        for rect, num in zip(rects, arr):
            # Put the value inside the box
            label = Text(str(num)).scale(0.9).move_to(rect)
            labels.add(label)
        self.play(Create(rects), Write(labels))
        return rects, labels

    def binary_search_visualization(self, rects, labels, arr, target):
        low = 0
        high = len(arr) - 1

        # Create arrows for left, mid, and right
        left_arrow = Arrow(start=DOWN, end=UP).next_to(rects[low], DOWN).set_color(LIGHT_GRAY)
        right_arrow = Arrow(start=DOWN, end=UP).next_to(rects[high], DOWN).set_color(DARK_GRAY)
        mid_arrow = Arrow(start=DOWN, end=UP).next_to(rects[(high+low)//2], DOWN).set_color(GREEN)
        self.play(Create(left_arrow), Create(right_arrow))
        self.play(Create(mid_arrow))

        while low <= high:
            mid = (high + low) // 2

            # Move mid arrow and color it yellow
            self.play(mid_arrow.animate.next_to(rects[mid], DOWN).set_opacity(1))
            self.play(rects[mid].animate.set_color(YELLOW), labels[mid].animate.set_color(BLACK))

            if arr[mid] < target:
                low = mid + 1
                
                # Hide mid arrow temporarily
                mid_arrow.set_opacity(0)
                
                # If not found, set the color 
                self.play(rects[mid].animate.set_color(GRAY), labels[mid].animate.set_color(WHITE))
                
                # Move left arrow
                if low < len(arr):
                    self.play(left_arrow.animate.next_to(rects[low], DOWN))
                else:
                    self.play(right_arrow.animate.next_to(rects[-1], DR))  # Off screen to the left
            elif arr[mid] > target:
                high = mid - 1
                
                # Hide mid arrow temporarily
                mid_arrow.set_opacity(0)
                
                # If not found, set the color 
                self.play(rects[mid].animate.set_color(GRAY), labels[mid].animate.set_color(WHITE))
                
                # Move right arrow
                if high >= 0:
                    self.play(right_arrow.animate.next_to(rects[high], DOWN))
                else:
                    self.play(right_arrow.animate.next_to(rects[0], DL))  # Off screen to the left
            else:
                self.play(rects[mid].animate.set_color(GREEN), labels[mid].animate.set_color(BLACK))
                self.play(Wiggle(rects[mid], scale_value=2, rotation_angle=0.05*TAU, n_wiggles=5, run_time=2), Wiggle(labels[mid], scale_value=2, rotation_angle=0.05*TAU, n_wiggles=5, run_time=2))
                # self.play(Wiggle(rects[mid], scale_value=1.2, rotation_angle=0.05*TAU, n_wiggles=3, run_time=1))
                return mid

        self.play(Wiggle(rects, scale_value=1.2, rotation_angle=0.05*TAU, n_wiggles=5, run_time=2), Wiggle(labels, scale_value=1.2, rotation_angle=0.05*TAU, n_wiggles=5, run_time=2))
        # self.play(Wiggle(rects, scale_value=1.2, rotation_angle=0.05*TAU, n_wiggles=3, run_time=1))
        return -1

from manim import *

def phi_of_vector(vector):
    vector += 1e-8
    xy = complex(*vector[:2])
    if xy == 0:
        return 0
    a = ((vector[:1])**2 + (vector[1:2])**2)**(1/2)
    vector[0] = a
    vector[1] = vector[2]
    return np.angle(complex(*vector[:2]))

class HyperPlane(ParametricSurface):

    def __init__(self, **kwargs):
        kwargs = {"u_min":-2, "u_max":2, "v_min":-2, "v_max":2}
        ParametricSurface.__init__(self, self.func, **kwargs)

    def func(self, x, y):
        return np.array([x,y,3*y])

class HyperPlane2(ParametricSurface):

    def __init__(self, **kwargs):
        kwargs = {"u_min":-2, "u_max":2, "v_min":-2, "v_max":2}
        ParametricSurface.__init__(self, self.func, **kwargs)

    def func(self, x, y):
        return np.array([x,y,-x/2])

class Introduction(Scene):

    def construct(self):
        title = Tex(r"Schrijver's Algorithm").scale(1.4).shift(UP*2)
        exp1 = Tex(r"Input: row vectors $\vec{a}_1,\ldots,\vec{a}_n, \vec{b}$." 
                + r"\\Tests if $\vec{b}\in\text{cone}\left\lbrace\vec{a}_1,\ldots,\vec{a}_n\right\rbrace$."
                + r"\\That is, the algorithm determines the feasibility"
                + r"\\of a system of linear equalities"
                + r"\\$A\vec{x}=\vec{b}$"
                + r"\\with nonnegativity constraints $\vec{x}\geq\vec{0}$,"
                + r"\\where $\vec{a}_1,\ldots,\vec{a}_n$ are the columns of $A$.").shift(DOWN)

        self.play(Write(title))
        self.play(Write(exp1),run_time=5)

        self.wait(1)

        self.play(FadeOut(title), FadeOut(exp1)) 

        self.wait(1)




class Example1(ThreeDScene):

    def construct(self):
        axes = ThreeDAxes(z_min=-5.5,z_max=5.5)

        self.set_camera_orientation(phi=PI/4, theta=PI/6)

        exp = Tex(r"We are going to use the following input:"
                + r"\\$\vec{a}_1=\begin{bmatrix}1\\1\\3\end{bmatrix},\vec{a}_2=\begin{bmatrix}1\\-1\\3\end{bmatrix},\vec{a}_3=\begin{bmatrix}-1\\1\\3\end{bmatrix},\vec{a}_4=\begin{bmatrix}-1\\-1\\3\end{bmatrix},\vec{b}=\begin{bmatrix}2\\2\\0\end{bmatrix}.$")

        a1 = Vector(np.array([1,1,3]),color=GOLD_D)
        a2 = Vector(np.array([1,-1,3]),color=GOLD_D)
        a3 = Vector(np.array([-1,1,3]),color=GOLD_D)
        a4 = Vector(np.array([-1,-1,3]),color=GOLD_D)

        b = Vector(np.array([2,2,0]),color=PURPLE_D)

        a1_label = MathTex(r"\vec{a}_1",color=GOLD_D).next_to(a1.tip,OUT*2/3).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a2_label = MathTex(r"\vec{a}_2",color=GOLD_D).next_to(a2.tip,OUT*2/3).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a3_label = MathTex(r"\vec{a}_3",color=GOLD_D).next_to(a3.tip,OUT*2/3).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a4_label = MathTex(r"\vec{a}_4",color=GOLD_D).next_to(a4.tip,OUT*2/3).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)

        b_label = MathTex(r"\vec{b}",color=PURPLE_D).next_to(b.tip,-RIGHT/8+OUT).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)

        caption1 = Tex(r"We find $\vec{a}_i$'s\\that span the whole space.").scale(0.7)

        caption2 = Tex(r"Write $\vec{b}$ as a linear combination\\of $\vec{a}_1, \vec{a}_2, \vec{a}_3$:").scale(0.7)

        lower_caption1 = Tex(r"\begin{align*}\vec{b}&=\lambda_1\vec{a}_1+\lambda_2\vec{a}_2+\lambda_3\vec{a}_3\\&=2\vec{a}_1-\vec{a}_2-\vec{a}_3\end{align*}").scale(0.7)

        caption3 = Tex(r"We have negative coefficients;\\find the smallest index\\$h\in\lbrace 1,2,3\rbrace$ such that $\lambda_h<0$:").scale(0.7)

        lower_caption2 = MathTex(r"h=2").scale(0.7)

        caption4 = Tex(r"Find $\vec{c}$ that is orthogonal to $\vec{a}_1,\vec{a}_3$\\and is such that $\vec{c}^T\vec{a}_h=\vec{c}^T\vec{a}_2>0$:").scale(0.7)

        lower_caption3 = MathTex(r"\vec{c}=\begin{bmatrix}0\\-3\\1\end{bmatrix}").scale(0.7)

        caption5 = Tex(r"Geometrically,\\we have a linear hyperplane\\spanned by $\vec{a}_1,\vec{a}_3$, which divides\\the whole space into two parts.").scale(0.7)
        caption5_below = Tex(r"We are finding $\vec{c}$ orthogonal to\\the hyperplane such that $\vec{c}$ lies\\on the same side as $\vec{a}_2$.").scale(0.7)
        caption5_next_to = Tex(r"This $\vec{c}$ is guaranteed to lie on\\the other side of $\vec{b}$\\by definition as well.").scale(0.7)

        c = Vector(np.array([0,-3,1]),color=MAROON_D)
        c_label = MathTex(r"\vec{c}",color=MAROON_D).next_to(c.tip,-RIGHT/8+OUT).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/8,axis=OUT)

        caption6 = Tex(r"Since we have found a hyperplane\\that \textit{separates} $\vec{b}$ from $\vec{a}_i$'s,\\we are done. $\vec{c}$ is a\\\textit{certificate} of the infeasibility.").scale(0.7)

        P = HyperPlane()

        self.wait(1)

        self.add_fixed_in_frame_mobjects(exp)
        self.play(Write(exp), run_time=2)

        self.wait(1)

        self.play(FadeOut(exp))

        self.wait(1)

        self.begin_ambient_camera_rotation(rate=-0.01)

        self.play(Create(axes))
        self.play(Create(a1),run_time=0.3)
        self.play(Write(a1_label),run_time=0.3)
        self.play(Create(a2),run_time=0.3)
        self.play(Write(a2_label),run_time=0.3)
        self.play(Create(a3),run_time=0.3)
        self.play(Write(a3_label),run_time=0.3)
        self.play(Create(a4),run_time=0.3)
        self.play(Write(a4_label),run_time=0.3)

        self.play(Create(b),run_time=0.3)
        self.play(Write(b_label),run_time=0.3)

        self.wait(1)

        self.add_fixed_in_frame_mobjects(caption1)
        caption1.to_corner(UL)
        self.play(Write(caption1))

        self.wait(1)

        self.play(ApplyMethod(a1.set_color, RED_D), ApplyMethod(a2.set_color, RED_D), ApplyMethod(a3.set_color, RED_D), ApplyMethod(a1_label.set_color, RED_D), ApplyMethod(a2_label.set_color, RED_D), ApplyMethod(a3_label.set_color, RED_D))

        self.wait(1)

        self.play(ApplyMethod(a1.set_color, GOLD_D), ApplyMethod(a2.set_color, GOLD_D), ApplyMethod(a3.set_color, GOLD_D), ApplyMethod(a1_label.set_color, GOLD_D), ApplyMethod(a2_label.set_color, GOLD_D), ApplyMethod(a3_label.set_color, GOLD_D))

        self.wait(1)

        self.play(FadeOut(caption1))
        self.add_fixed_in_frame_mobjects(caption2)
        caption2.to_corner(UL)
        self.play(Write(caption2))

        self.add_fixed_in_frame_mobjects(lower_caption1)
        lower_caption1.to_corner(DR)
        self.play(Write(lower_caption1))

        self.wait(1)

        self.play(FadeOut(caption2))
        self.add_fixed_in_frame_mobjects(caption3)
        caption3.to_corner(UL)
        self.play(Write(caption3))

        self.play(FadeOut(lower_caption1))
        self.add_fixed_in_frame_mobjects(lower_caption2)
        lower_caption2.to_corner(DR)
        self.play(Write(lower_caption2))

        self.play(ApplyMethod(a2.set_color, RED_D), ApplyMethod(a2_label.set_color, RED_D))
        self.play(ApplyMethod(a2.set_color, GOLD_D), ApplyMethod(a2_label.set_color, GOLD_D))

        self.wait(1)

        self.play(FadeOut(caption3))
        self.add_fixed_in_frame_mobjects(caption4)
        caption4.to_corner(UL)
        self.play(Write(caption4))

        self.play(FadeOut(lower_caption2))
        self.add_fixed_in_frame_mobjects(lower_caption3)
        lower_caption3.to_corner(DR)
        self.play(Write(lower_caption3))

        self.wait(1)

        self.play(FadeOut(caption4))
        self.add_fixed_in_frame_mobjects(caption5)
        caption5.to_corner(UL)
        self.play(Write(caption5))

        self.play(Create(P))

        self.wait(1)

        self.add_fixed_in_frame_mobjects(caption5_below)
        caption5_below.to_corner(DL)
        self.play(Write(caption5_below))

        self.play(Create(c))
        self.play(Write(c_label))

        self.wait(1)

        self.add_fixed_in_frame_mobjects(caption5_next_to)
        caption5_next_to.to_corner(UR)
        self.play(Write(caption5_next_to))

        self.wait(1)

        self.play(FadeOut(caption5), FadeOut(caption5_below), FadeOut(caption5_next_to))
        self.add_fixed_in_frame_mobjects(caption6)
        caption6.to_corner(UL)
        self.play(Write(caption6))

        self.wait(2)
        self.play(FadeOut(caption6), FadeOut(lower_caption3), FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(a4), FadeOut(b), FadeOut(c), 
                FadeOut(a1_label), FadeOut(a2_label), FadeOut(a3_label), FadeOut(a4_label), FadeOut(b_label), FadeOut(c_label), FadeOut(axes), FadeOut(P), run_time=3)


class Example2(ThreeDScene):

    def construct(self):
        axes = ThreeDAxes(z_min=-5.5,z_max=5.5)

        self.set_camera_orientation(phi=PI/4, theta=PI/6)

        exp = Tex(r"We are going to use the following input:"
                + r"\\$\vec{a}_1=\begin{bmatrix}2\\2\\1\end{bmatrix},\vec{a}_2=\begin{bmatrix}2\\0\\-1\end{bmatrix},\vec{a}_3=\begin{bmatrix}0\\2\\-1\end{bmatrix},\vec{a}_4=\begin{bmatrix}-2\\0\\-1\end{bmatrix},\vec{a}_5=\begin{bmatrix}-2\\-2\\1\end{bmatrix},\vec{b}=\begin{bmatrix}2\\2\\0\end{bmatrix}.$")

        a1 = Vector(np.array([1,1,3]),color=GOLD_D)

        a1 = Vector(np.array([2,2,1]),color=GOLD_D)
        a2 = Vector(np.array([2,0,-1]),color=GOLD_D)
        a3 = Vector(np.array([0,2,-1]),color=GOLD_D)
        a4 = Vector(np.array([-2,0,-1]),color=GOLD_D)
        a5 = Vector(np.array([-2,-2,-1]),color=GOLD_D)

        b = Vector(np.array([1,1,-1]),color=PURPLE_D)

        a1_label = MathTex(r"\vec{a}_1",color=GOLD_D).next_to(a1.tip,OUT*2+UP/2+RIGHT/2).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a2_label = MathTex(r"\vec{a}_2",color=GOLD_D).next_to(a2.tip,OUT*2+UP/2        ).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a3_label = MathTex(r"\vec{a}_3",color=GOLD_D).next_to(a3.tip,OUT*2+     RIGHT/2).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a4_label = MathTex(r"\vec{a}_4",color=GOLD_D).next_to(a4.tip,OUT*2-UP/2        ).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)
        a5_label = MathTex(r"\vec{a}_5",color=GOLD_D).next_to(a5.tip,OUT*2-UP/2-RIGHT/2).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)

        b_label = MathTex(r"\vec{b}",color=PURPLE_D).next_to(b.tip,OUT*2+UP/2+RIGHT/2).rotate(PI,axis=OUT).rotate(-PI/2, axis=RIGHT).rotate(-PI/4,axis=OUT)

        caption1 = Tex(r"We find $\vec{a}_i$'s\\that span the whole space.").scale(0.7)

        caption2 = Tex(r"Write $\vec{b}$ as a linear combination\\of $\vec{a}_1, \vec{a}_4, \vec{a}_5$:").scale(0.7)

        lower_caption1 = Tex(r"\begin{align*}\vec{b}&=\lambda_1\vec{a}_1+\lambda_4\vec{a}_4+\lambda_5\vec{a}_5\\&=\frac{-1}{4}\vec{a}_1+0\vec{a}_4+\frac{-3}{4}\vec{a}_5\end{align*}").scale(0.7)

        caption3 = Tex(r"We have negative coefficients;\\find the smallest index\\$h\in\lbrace 1,4,5\rbrace$ such that $\lambda_h<0$:").scale(0.7)

        lower_caption2 = MathTex(r"h=1").scale(0.7)

        caption4 = Tex(r"Find $\vec{c}$ that is orthogonal to $\vec{a}_4,\vec{a}_5$\\and is such that $\vec{c}^T\vec{a}_h=\vec{c}^T\vec{a}_1>0$:").scale(0.7)

        lower_caption3 = MathTex(r"\vec{c}=\begin{bmatrix}\frac{1}{2}\\0\\1\end{bmatrix}").scale(0.7)

        c = Vector(np.array([1/2,0,1]),color=MAROON_D)
        c_label = MathTex(r"\vec{c}",color=MAROON_D).next_to(c.tip,-RIGHT/8+OUT).rotate(PI,axis=OUT).rotate(-PI/2,axis=RIGHT).rotate(-PI/8,axis=OUT)

        P = HyperPlane2()

        caption5 = Tex(r"Since the hyperplane does not\\separate $\vec{b}$ from $\vec{a}_i$'s, we are not done.").scale(0.7)

        caption6 = Tex(r"Find the smallest index\\$s\in\lbrace 1,\ldots,5\rbrace$ such that\\$\vec{c}^T\vec{a}_s<0$.\\Replace $\vec{a}_h=\vec{a}_1$ with $\vec{a}_s=\vec{a}_3$").scale(0.7)

        lower_caption4 = MathTex(r"s=3").scale(0.7)

        caption7 = Tex(r"Write $\vec{b}$ as a linear combination\\of $\vec{a}_3, \vec{a}_4, \vec{a}_5$:").scale(0.7)

        lower_caption5 = Tex(r"\begin{align*}\vec{b}&=\lambda_3\vec{a}_3+\lambda_4\vec{a}_2+\lambda_5\vec{a}_3\\&=\frac{1}{2}\vec{a}_3+0\vec{a}_4+1\vec{a}_5\end{align*}").scale(0.7)

        caption8 = Tex(r"Since every coefficient are nonnegative,\\we are done:\\$\vec{b}\in\text{cone}\lbrace\vec{a}_3,\vec{a}_4,\vec{a}_5\rbrace=\text{cone}\lbrace\vec{a}_1,\ldots,\vec{a}_5\rbrace.$").scale(0.7)

        self.wait(1)

        self.add_fixed_in_frame_mobjects(exp)
        self.play(Write(exp), run_time=2)

        self.wait(1)

        self.play(FadeOut(exp))

        self.wait(1)

        self.play(Create(axes))
        self.play(Create(a1),run_time=0.3)
        self.play(Write(a1_label),run_time=0.3)
        self.play(Create(a2),run_time=0.3)
        self.play(Write(a2_label),run_time=0.3)
        self.play(Create(a3),run_time=0.3)
        self.play(Write(a3_label),run_time=0.3)
        self.play(Create(a4),run_time=0.3)
        self.play(Write(a4_label),run_time=0.3)
        self.play(Create(a5),run_time=0.3)
        self.play(Write(a5_label),run_time=0.3)

        self.play(Create(b),run_time=0.3)
        self.play(Write(b_label),run_time=0.3)

        self.wait(1)

        self.play(ApplyMethod(a1_label.rotate, -PI/4, {"axis":OUT}), ApplyMethod(a2_label.rotate, -PI/4, {"axis":OUT}), ApplyMethod(a3_label.rotate, -PI/4, {"axis":OUT}), 
                ApplyMethod(a4_label.rotate, -PI/4, {"axis":OUT}), ApplyMethod(a5_label.rotate, -PI/4, {"axis":OUT}), ApplyMethod(b_label.rotate, -PI/4, {"axis":OUT}))
        self.play(ApplyMethod(a1_label.rotate, PI/2, {"axis":DOWN}), ApplyMethod(a2_label.rotate, PI/2, {"axis":DOWN}), ApplyMethod(a3_label.rotate, PI/2, {"axis":DOWN}), 
                ApplyMethod(a4_label.rotate, PI/2, {"axis":DOWN}), ApplyMethod(a5_label.rotate, PI/2, {"axis":DOWN}), ApplyMethod(b_label.rotate, PI/2, {"axis":DOWN}))
        self.move_camera(phi=0, theta=0)
        self.wait(2)

        self.play(ApplyMethod(a1_label.rotate, -PI/2, {"axis":DOWN}), ApplyMethod(a2_label.rotate, -PI/2, {"axis":DOWN}), ApplyMethod(a3_label.rotate, -PI/2, {"axis":DOWN}), 
                ApplyMethod(a4_label.rotate, -PI/2, {"axis":DOWN}), ApplyMethod(a5_label.rotate, -PI/2, {"axis":DOWN}), ApplyMethod(b_label.rotate, -PI/2, {"axis":DOWN}))
        self.play(ApplyMethod(a1_label.rotate, PI/4, {"axis":OUT}), ApplyMethod(a2_label.rotate, PI/4, {"axis":OUT}), ApplyMethod(a3_label.rotate, PI/4, {"axis":OUT}), 
                ApplyMethod(a4_label.rotate, PI/4, {"axis":OUT}), ApplyMethod(a5_label.rotate, PI/4, {"axis":OUT}), ApplyMethod(b_label.rotate, PI/4, {"axis":OUT}))
        self.move_camera(phi=PI/4, theta=PI/6)

        self.begin_ambient_camera_rotation(rate=0.02)

        self.wait(1)

        self.add_fixed_in_frame_mobjects(caption1)
        caption1.to_corner(UL)
        self.play(Write(caption1))

        self.wait(1)

        self.play(ApplyMethod(a1.set_color, RED_D), ApplyMethod(a4.set_color, RED_D), ApplyMethod(a5.set_color, RED_D), ApplyMethod(a1_label.set_color, RED_D), ApplyMethod(a4_label.set_color, RED_D), ApplyMethod(a5_label.set_color, RED_D))

        self.wait(1)

        self.play(ApplyMethod(a1.set_color, GOLD_D), ApplyMethod(a4.set_color, GOLD_D), ApplyMethod(a5.set_color, GOLD_D), ApplyMethod(a1_label.set_color, GOLD_D), ApplyMethod(a4_label.set_color, GOLD_D), ApplyMethod(a5_label.set_color, GOLD_D))

        self.wait(1)

        self.play(FadeOut(caption1))
        self.add_fixed_in_frame_mobjects(caption2)
        caption2.to_corner(UL)
        self.play(Write(caption2))

        self.add_fixed_in_frame_mobjects(lower_caption1)
        lower_caption1.to_corner(DR)
        self.play(Write(lower_caption1))

        self.wait(1)

        self.play(FadeOut(caption2))
        self.add_fixed_in_frame_mobjects(caption3)
        caption3.to_corner(UL)
        self.play(Write(caption3))

        self.play(FadeOut(lower_caption1))
        self.add_fixed_in_frame_mobjects(lower_caption2)
        lower_caption2.to_corner(DR)
        self.play(Write(lower_caption2))

        self.play(ApplyMethod(a1.set_color, RED_D), ApplyMethod(a1_label.set_color, RED_D))
        self.play(ApplyMethod(a1.set_color, GOLD_D), ApplyMethod(a1_label.set_color, GOLD_D))

        self.wait(1)

        self.play(FadeOut(caption3))
        self.add_fixed_in_frame_mobjects(caption4)
        caption4.to_corner(UL)
        self.play(Write(caption4))

        self.play(FadeOut(lower_caption2))
        self.add_fixed_in_frame_mobjects(lower_caption3)
        lower_caption3.to_corner(DR)
        self.play(Write(lower_caption3))

        self.wait(1)

        self.play(FadeOut(caption4))
        self.add_fixed_in_frame_mobjects(caption5)
        caption5.to_corner(UL)
        self.play(Write(caption5))

        self.play(Create(P))

        self.wait(1)

        self.play(Create(c))
        self.play(Write(c_label))

        self.play(FadeOut(caption5))
        self.add_fixed_in_frame_mobjects(caption6)
        caption6.to_corner(UL)
        self.play(Write(caption6))

        self.play(ApplyMethod(a1.set_color, GREEN_D), ApplyMethod(a1_label.set_color, GREEN_D), ApplyMethod(a3.set_color, RED_D), ApplyMethod(a3_label.set_color, RED_D))

        self.wait(1)

        self.play(ApplyMethod(a1.set_color, GOLD_D), ApplyMethod(a1_label.set_color, GOLD_D), ApplyMethod(a3.set_color, GOLD_D), ApplyMethod(a3_label.set_color, GOLD_D))

        self.wait(1)

        self.play(FadeOut(lower_caption3))
        self.add_fixed_in_frame_mobjects(lower_caption4)
        lower_caption4.to_corner(DR)
        self.play(Write(lower_caption4))

        self.wait(1)

        self.play(FadeOut(caption6))
        self.add_fixed_in_frame_mobjects(caption7)
        caption7.to_corner(UL)
        self.play(Write(caption7))

        self.play(FadeOut(lower_caption4))
        self.add_fixed_in_frame_mobjects(lower_caption5)
        lower_caption5.to_corner(DR)
        self.play(Write(lower_caption5))

        self.wait(1)

        self.play(FadeOut(caption7))
        self.add_fixed_in_frame_mobjects(caption8)
        caption8.to_corner(UL)
        self.play(Write(caption8))

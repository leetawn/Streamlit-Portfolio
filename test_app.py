"""
Smoke test suite for Autobiography and Portfolio Streamlit app.
Uses streamlit.testing.v1.AppTest.
"""

from streamlit.testing.v1 import AppTest

def test_app_smoke():
    at = AppTest.from_file("app.py", default_timeout=30)
    at.run()
    assert not at.exception, f"App execution failed with exception: {at.exception}"
    
    # Check title
    assert len(at.title) >= 1, f"Expected st.title, got {len(at.title)}"
    
    # Check tabs
    assert len(at.tabs) == 5, f"Expected 5 tabs, got {len(at.tabs)}"
    
    # Check metrics
    assert len(at.metric) >= 4, f"Expected at least 4 metrics, got {len(at.metric)}"
    
    # Test random fun fact button
    fun_fact_btn = [b for b in at.button if b.key == "btn_fun_fact"][0]
    fun_fact_btn.click().run()
    assert not at.exception, f"Fun fact button failed: {at.exception}"
    

    # Test skills filters
    cat_ms = [m for m in at.multiselect if m.key == "skills_category_multiselect"][0]
    cat_ms.set_value(["Programming Languages", "AI & Data Science"]).run()
    assert not at.exception, f"Skills multiselect failed: {at.exception}"
    
    level_slider = [s for s in at.slider if s.key == "skills_level_slider"][0]
    level_slider.set_value(75).run()
    assert not at.exception, f"Skills slider failed: {at.exception}"
    
    top_chk = [c for c in at.checkbox if c.key == "skills_top_tier_checkbox"][0]
    top_chk.check().run()
    assert not at.exception, f"Skills checkbox failed: {at.exception}"
    top_chk.uncheck().run()
    assert not at.exception, f"Skills checkbox uncheck failed: {at.exception}"
    
    chart_radio = [r for r in at.radio if r.key == "skills_chart_radio"][0]
    chart_radio.set_value("Area Chart").run()
    assert not at.exception, f"Chart radio switch failed: {at.exception}"
    
    chart_radio.set_value("Bar Chart").run()
    assert not at.exception, f"Chart radio switch back failed: {at.exception}"
    
    # Test project tool filter
    tool_ms = [m for m in at.multiselect if m.key == "projects_tool_filter"][0]
    tool_ms.set_value(["C", "Godot"]).run()
    assert not at.exception, f"Projects multiselect failed: {at.exception}"
    
    # Test contact form submission
    at.text_input[0].input("Jane Doe")
    at.text_input[1].input("jane@example.com")
    at.text_area[0].input("This portfolio looks awesome and well structured!")
    
    # Submit button
    submit_btn = [b for b in at.button if "FormSubmitter:contact_form" in str(b.key)][0]
    submit_btn.click().run()
    assert not at.exception, f"Form submission failed: {at.exception}"
    
    # Verify feedback messages updated
    assert len(at.session_state.feedback_messages) == 1
    assert at.session_state.feedback_messages[0]["Name"] == "Jane Doe"
    assert at.session_state.feedback_messages[0]["Rating"] == 5
    
    print("All AppTest smoke tests PASSED successfully!")

if __name__ == "__main__":
    test_app_smoke()

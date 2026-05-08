from app.core.schemas import AgentState, ValidationResult

def router_node(state: AgentState) -> AgentState:
    print(f"\n--- [NODE] Final Routing Decision ---")
    
    # Lấy dữ liệu từ cả 2 nguồn "thông tin thiếu"
    customer_missing = state.draft_data.missing_info    # Khách hàng thiếu
    ai_missing_policy = state.validation_data.missing_info # AI viết thiếu
    is_valid = state.validation_data.is_valid
    priority = state.priority_data.level
    confidence = state.intent_data.confidence

    decision = ""
    reason = ""
    
# 1. TRƯỜNG HỢP GỬI THẲNG (Ưu tiên tự động hóa)
    # Ngay cả khi High Priority, nếu AI làm CỰC TỐT (Valid và Confidence cao) thì vẫn cho gửi.
    if is_valid and confidence > 0.8 and customer_missing.lower() == "none":
        decision = "send_reply_directly"
        reason = "High confidence & Validated response. Safe to automate."

    # 2. TRƯỜNG HỢP HỎI THÊM (Giảm tải cho người thật)
    # Nếu khách thiếu thông tin, cứ để AI hỏi, không việc gì phải làm phiền nhân viên.
    elif customer_missing.lower() != "none" and customer_missing.strip() != "":
        decision = "ask_for_more_info"
        reason = f"AI identified missing customer data: {customer_missing}"

    # 3. TRƯỜNG HỢP CHUYỂN NGƯỜI THẬT (Chỉ khi thực sự cần thiết)
    # Chỉ chuyển khi: (Nguy cơ cao VÀ AI không tự tin) HOẶC (AI sai kiến thức nghiêm trọng - is_valid=False)
    elif priority == "high" and confidence < 0.7:
        decision = "escalate_to_human"
        reason = "High priority case with low AI confidence. Needs expert handling."
    
    elif not is_valid:
        # Nếu AI viết sai policy hoặc trả về quá ngắn
        decision = "escalate_to_human"
        reason = f"Quality check failed: {state.validation_data.feedback}"

    # 4. TRƯỜNG HỢP DỰ PHÒNG (Fallback)
    else:
        # Nếu không rơi vào các case trên, thường là các case Medium/Low mà AI làm ổn
        decision = "send_reply_directly"
        reason = "Standard case handled by AI."

    state.metadata["final_decision"] = decision
    print(f"Final Decision: {decision.upper()} ({reason})")
    return state